import re
from nltk.stem import PorterStemmer
# from nltk.tokenize import word_tokenize
import re

stemmer = PorterStemmer()

def tokenize_and_stem(text):
    # Clean and tokenize
    tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
    cleaned = [re.sub(r'\W+', '', token.lower()) for token in tokens if token.isalnum()]
    return [stemmer.stem(token) for token in cleaned if token]
