import os
import shutil
import pandas as pd
from flask import Blueprint, request, jsonify, send_from_directory, send_file

from config import Config
from nlp.processor import detect_similarity, load_spacy_model
from services.cv_service import load_cv_data, get_recommended_cvs

api = Blueprint('api', __name__)

matched_cvs_storage = {}
positions_storage = {}

nlp_model = load_spacy_model()


@api.route('/upload-cv', methods=['POST'])
def upload_cv():
    global matched_cvs_storage
    global positions_storage

    matched_cvs_storage = {}
    positions_storage = {}

    for filename in os.listdir(Config.PUBLIC_FOLDER):
        file_path = os.path.join(Config.PUBLIC_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            return jsonify({"error": f"Failed to delete {file_path}. Reason: {e}"}), 500

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist('file')
    if not files:
        return jsonify({"error": "No selected file"}), 400

    uploaded_files = []
    for file in files:
        if file and file.filename.endswith('.docx'):
            filename = file.filename
            file.save(os.path.join(Config.PUBLIC_FOLDER, filename))
            uploaded_files.append({
                "message": "File uploaded successfully",
                "file_path": os.path.join(Config.PUBLIC_FOLDER, filename)
            })

    if not uploaded_files:
        return jsonify({"error": "Invalid file format. Only .docx files are allowed."}), 400

    return jsonify(uploaded_files), 200


@api.route('/enter-positions', methods=['POST'])
def enter_positions():
    data = request.json
    position = data.get('position')

    if not position:
        return jsonify({"error": "Position is required"}), 400

    positions_storage['position'] = position
    return jsonify({"message": "Position stored successfully", "position": position}), 200


@api.route('/match-cvs', methods=['POST'])
def match_cvs():
    data = request.json
    skills = data.get('skills')

    if not skills:
        return jsonify({"error": "Skills are required"}), 400

    position = positions_storage.get('position')
    if not position:
        return jsonify({"error": "Position is not entered. Please enter position first."}), 400

    cv_data = load_cv_data(Config.PUBLIC_FOLDER)
    if not cv_data:
        return jsonify({"error": "No CV data found in the uploaded folder"}), 404

    cv_matches = detect_similarity(skills, cv_data, nlp_model)
    similar_cvs = get_recommended_cvs(cv_matches, position)

    if not similar_cvs:
        return jsonify({"message": "No CVs found matching the entered skills"}), 404

    matched_cvs_storage['cvs'] = similar_cvs
    matched_cvs_storage['position'] = position

    return jsonify(similar_cvs)


@api.route('/get-matched-cvs', methods=['GET'])
def get_matched_cvs():
    if 'cvs' not in matched_cvs_storage or not matched_cvs_storage['cvs']:
        return jsonify({"error": "No matched CVs found. Please run the match-cvs endpoint first."}), 400

    position = matched_cvs_storage.get('position', 'N/A')
    results = []

    for cv_info in matched_cvs_storage['cvs']:
        contact_info = cv_info['contact_info']
        results.append({
            "position": position,
            "file_name": cv_info['file_name'],
            "file_path": f"/{Config.UPLOAD_FOLDER}/{cv_info['file_name']}",
            "contact_info": {
                "email": contact_info.get('email', 'N/A'),
                "phone_number": contact_info.get('phone_number', 'N/A')
            },
            "matched_skills": cv_info['matched_skills']
        })

    return jsonify(results)


@api.route('/export-to-excel', methods=['GET'])
def export_to_excel():
    if 'cvs' not in matched_cvs_storage or not matched_cvs_storage['cvs']:
        return jsonify({"error": "No matched CVs found. Please run the match-cvs endpoint first."}), 400

    position = matched_cvs_storage.get('position', 'N/A')
    data = matched_cvs_storage['cvs']
    export_data = []

    for cv_info in data:
        contact_info = cv_info['contact_info']
        export_data.append({
            "Position": position,
            "Email": contact_info.get('email', 'N/A'),
            "Phone Number": contact_info.get('phone_number', 'N/A')
        })

    df = pd.DataFrame(export_data)
    excel_filename = "matched_cvs.xlsx"
    excel_path = os.path.join(Config.PUBLIC_FOLDER, excel_filename)
    df.to_excel(excel_path, index=False)

    return send_file(excel_path, as_attachment=True)


@api.route(f'/{Config.UPLOAD_FOLDER}/<filename>')
def uploaded_file(filename):
    return send_from_directory(Config.PUBLIC_FOLDER, filename)
