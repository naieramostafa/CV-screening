import os
from docx import Document
from nlp.processor import preprocess_cv


def load_cv_data(folder_path):
    file_names = os.listdir(folder_path)
    cv_data = []
    for file_name in file_names:
        if file_name.endswith('.docx'):
            file_path = os.path.join(folder_path, file_name)
            doc = Document(file_path)
            cv_text = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
            skills, contact_info = preprocess_cv(cv_text)
            cv_data.append((skills, contact_info, file_name, file_path))
    return cv_data


def get_recommended_cvs(cv_matches, position):
    sorted_scores = sorted(cv_matches.keys(), reverse=True)
    recommended_cvs = []

    for score in sorted_scores:
        if score > 0:
            for cv_info in cv_matches[score]:
                skills, contact_info, file_name, file_path, matched_skills = cv_info
                unique_matched_skills = list(set(matched_skills))

                recommended_cvs.append({
                    "position": position,
                    "file_name": file_name,
                    "contact_info": {
                        "email": contact_info.get('email', 'N/A'),
                        "phone_number": contact_info.get('phone_number', 'N/A')
                    },
                    "matched_skills": unique_matched_skills
                })

    return recommended_cvs
