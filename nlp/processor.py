import nltk
import spacy
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz
from config import Config


def download_nltk_data():
    try:
        stopwords.words('english')
    except LookupError:
        nltk.download('stopwords')
    try:
        word_tokenize("test")
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/wordnet.zip')
    except LookupError:
        nltk.download('wordnet')


def load_spacy_model():
    return spacy.load(Config.SPACY_MODEL)


def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms


def preprocess_cv(cv_text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    skills = []
    contact_info = {}

    for line in cv_text:
        words = word_tokenize(line)
        words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
        words = [lemmatizer.lemmatize(word) for word in words]

        if line.startswith("3."):
            if "SkillName" in line:
                skill_info = line.split(":")
                if len(skill_info) >= 2:
                    skill_name = skill_info[1].strip()
                    skills.append(skill_name)
        elif line.lower().startswith("full name:"):
            contact_info['full_name'] = line.split(":")[1].strip()
        elif line.lower().startswith("address:"):
            contact_info['address'] = line.split(":")[1].strip()
        elif line.lower().startswith("phone number:"):
            contact_info['phone_number'] = line.split(":")[1].strip()
        elif line.lower().startswith("email:"):
            contact_info['email'] = line.split(":")[1].strip()

    return skills, contact_info


def preprocess_entered_skills(entered_skills, nlp_model):
    processed_skills = []
    for skill in entered_skills:
        doc = nlp_model(skill.lower())
        processed_skills.append(doc)
    return processed_skills


def detect_similarity(entered_skills, cv_data, nlp_model):
    from collections import defaultdict

    entered_skills_processed = preprocess_entered_skills(entered_skills, nlp_model)
    cv_matches = defaultdict(list)

    for skills, contact_info, file_name, file_path in cv_data:
        cv_skills = [skill.lower() for skill in skills]
        common_skills = []

        for entered_skill in entered_skills_processed:
            found_match = False
            for cv_skill in cv_skills:
                doc_cv_skill = nlp_model(cv_skill)
                similarity_score = entered_skill.similarity(doc_cv_skill)
                if similarity_score >= Config.SIMILARITY_THRESHOLD:
                    common_skills.append(cv_skill)
                    found_match = True
                    break

            if not found_match:
                for cv_skill in cv_skills:
                    if fuzz.partial_ratio(entered_skill.text, cv_skill) >= Config.FUZZY_THRESHOLD:
                        common_skills.append(cv_skill)
                        found_match = True
                        break

        match_score = len(common_skills) / len(entered_skills) if entered_skills else 0
        cv_matches[match_score].append((skills, contact_info, file_name, file_path, common_skills))

    return cv_matches
