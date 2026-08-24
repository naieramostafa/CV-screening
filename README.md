# CV Screening System

A Flask-based API for automated CV/Resume screening using NLP and fuzzy matching.

## Project Structure

```
CV-screening/
├── app.py                  # Application entry point
├── config.py               # Configuration settings
├── README.md
├── requirements.txt
├── api/
│   ├── __init__.py
│   └── routes.py           # Flask API endpoints
├── nlp/
│   ├── __init__.py
│   └── processor.py        # NLP processing (tokenization, similarity)
├── services/
│   ├── __init__.py
│   └── cv_service.py       # CV loading and matching logic
└── utils/
    ├── __init__.py
    └── helpers.py           # Utility functions
```

## Features

- Upload CVs (DOCX format)
- Extract skills and contact information
- Match CVs against job requirements
- NLP-based similarity detection
- Fuzzy matching fallback
- Export matched results to Excel

## API Endpoints

- `POST /upload-cv` - Upload CV files
- `POST /enter-positions` - Set job position
- `POST /match-cvs` - Match CVs with skills
- `GET /get-matched-cvs` - Get matched results
- `GET /export-to-excel` - Export to Excel

## Requirements

- Python 3.8+
- Flask
- flask-cors
- python-docx
- nltk
- spacy
- fuzzywuzzy
- pandas
- openpyxl

## Installation

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

## Usage

```bash
python app.py
```
