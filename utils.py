import re
from nltk.stem import PorterStemmer
# from nltk.tokenize import word_tokenize
import re

# stemmer = PorterStemmer()
# STOPWORDS = set([
#     "the", "is", "in", "and", "of", "a", "an", "to", "for", "on", "with", "by",
#     "from", "that", "this", "at", "as", "are", "be", "it", "was", "or", "but",
#     "so", "do", "have", "has", "had", "not", "if", "i", "you", "we", "they",
#     "he", "she", "what", "can", "will", "please", "help"
# ])

# def tokenize_and_stem_for_indexing(text):
#     tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
#     cleaned = [re.sub(r'\W+', '', token) for token in tokens if token.isalnum()]
#     return [stemmer.stem(token) for token in cleaned if token and token not in STOPWORDS]

# def tokenize_and_stem_for_search(text):
#     tokens = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
#     cleaned = [re.sub(r'\W+', '', token) for token in tokens if token.isalnum()]
#     return [stemmer.stem(token) for token in cleaned if token]



'''works with searching "the" '''
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

