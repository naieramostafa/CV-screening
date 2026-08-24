import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    UPLOAD_FOLDER = 'uploaded_cvs'
    PUBLIC_FOLDER = os.path.join('static', UPLOAD_FOLDER)
    ALLOWED_EXTENSIONS = {'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    SPACY_MODEL = 'en_core_web_md'
    SIMILARITY_THRESHOLD = 0.7
    FUZZY_THRESHOLD = 80

    PORT = int(os.environ.get("PORT", 10000))
    HOST = "0.0.0.0"
