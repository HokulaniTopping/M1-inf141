# import os, json
# from bs4 import BeautifulSoup
# from nltk.stem import PorterStemmer
# from nltk.tokenize import word_tokenize
# from collections import defaultdict
# import re

# stemmer = PorterStemmer()
# index = defaultdict(list)

# def clean_text(text):
#     return re.findall(r'\b\w+\b', text.lower())

# def process_file(filename, doc_id):
#     with open(filename, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#         soup = BeautifulSoup(data['content'], 'html.parser')
#         tokens = clean_text(soup.get_text())
#         freq = defaultdict(int)
#         for token in tokens:
#             stem = stemmer.stem(token)
#             freq[stem] += 1
#         for term, count in freq.items():
#             index[term].append((doc_id, count))
 
# doc_id = 0
# for root, _, files in os.walk('ANALYST'):
#     for file in files:
#         if file.endswith('.json'):
#             process_file(os.path.join(root, file), doc_id)
#             doc_id += 1

            


import os
import json
import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import defaultdict
from utils import tokenize_and_stem

DATA_DIR = "data"
OUTPUT_INDEX = "index.json"

def process_file(filepath, doc_id):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            html = data.get('content', '')
            url = data.get('url', f'doc_{doc_id}')
            text = BeautifulSoup(html, 'html.parser').get_text()
            tokens = tokenize_and_stem(text)

            term_freqs = defaultdict(int)
            for token in tokens:
                term_freqs[token] += 1

            return url, term_freqs

        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            return None, {}

def build_index():
    index = defaultdict(list)
    doc_id_map = {}
    doc_id = 0

    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".json"):
                filepath = os.path.join(root, file)
                url, term_freqs = process_file(filepath, doc_id)
                if url:
                    doc_id_map[doc_id] = url
                    for term, freq in term_freqs.items():
                        index[term].append({'doc_id': doc_id, 'tf': freq})
                    doc_id += 1

    return index, doc_id_map

def save_index(index, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)

def save_doc_map(doc_id_map, path="doc_ids.json"):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(doc_id_map, f, indent=2)

if __name__ == "__main__":
    print("Building inverted index...")
    index, doc_id_map = build_index()
    save_index(index, OUTPUT_INDEX)
    save_doc_map(doc_id_map)
    print(f"Index saved to {OUTPUT_INDEX}")
    print(f"Total documents indexed: {len(doc_id_map)}")
    print(f"Total unique tokens: {len(index)}")
