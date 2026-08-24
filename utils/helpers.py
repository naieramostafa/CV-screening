import os
import nltk
from nltk.corpus import stopwords


def download_nltk_data():
    try:
        stopwords.words('english')
    except LookupError:
        nltk.download('stopwords')
    try:
        nltk.tokenize.word_tokenize("test")
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/wordnet.zip')
    except LookupError:
        nltk.download('wordnet')
