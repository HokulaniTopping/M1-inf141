

import os
import json
import re
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from nltk.stem import PorterStemmer
# from nltk.tokenize import word_tokenize
from collections import defaultdict
from utils import tokenize_and_stem
import warnings



DATA_DIR = "ANALYST"
OUTPUT_INDEX = "index.json"
REPORT_INDEX  = "report.txt"

def process_file(filepath, doc_id):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            html = data.get('content', '')
            url = data.get('url', f'doc_{doc_id}')
            warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
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

    for root, _, files in os.walk('ANALYST'):
        for file in files:
            if file.endswith(".json"):
                filepath = os.path.join(root, file)
                url, term_freqs = process_file(filepath, doc_id)
                if url:
                    doc_id_map[doc_id] = url
                    for term, freq in term_freqs.items():
                        index[term].append({'doc_id': doc_id, 'term_freq': freq})
                    doc_id += 1

    return index, doc_id_map


def save_report(path, doc_count, token_count, index_path):

    size_kb = os.path.getsize(index_path) / 1024

    with open(path, 'w') as f:
        f.write("Milestone 1 Report\n")
        f.write("===================\n")
        f.write(f"Number of indexed documents: {doc_count}\n")
        f.write(f"Number of unique tokens: {token_count}\n")
        f.write(f"Size of index on disk: {size_kb} KB\n")



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
    save_report(REPORT_INDEX, len(doc_id_map), len(index), OUTPUT_INDEX)
    print(f"Index saved to {OUTPUT_INDEX}")
    print(f"Total documents indexed: {len(doc_id_map)}")
    print(f"Total unique tokens: {len(index)}")
    print(f"Report saved to {REPORT_INDEX}")
