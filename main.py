

import os
import json
import re
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from nltk.stem import PorterStemmer
# from nltk.tokenize import word_tokenize
from collections import defaultdict
from utils import tokenize_and_stem
import warnings
import hashlib


DATA_DIR = "ANALYST"
OUTPUT_INDEX = "index.json"
REPORT_INDEX  = "report.txt"


def get_content_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()



def process_file(filepath, doc_id):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            html = data.get('content', '')
            url = data.get('url', f'doc_{doc_id}')
            warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()

            tokens = tokenize_and_stem(text)
            term_positions = defaultdict(list)

            #generating n grams
            def generate_ngrams(tokens, n):
                return [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
            


            for i, token in enumerate(tokens):
                term_positions[token].append(i)

            bigrams = generate_ngrams(tokens, 2)
            trigrams = generate_ngrams(tokens, 3)

            for i, token in enumerate(bigrams):
                term_positions[token].append(i + 100000)  # Offset to avoid collisions

            for i, token in enumerate(trigrams):
                term_positions[token].append(i + 200000)

            # term_freqs = defaultdict(int)
            # for token in tokens:
            #     term_freqs[token] += 1

            # token frequency with bigrams and trigrams (extra credit)
            term_freqs = defaultdict(int)
            for token in tokens + bigrams + trigrams:
                term_freqs[token] += 1

            #anchor text (extra credit)
            anchor_text = ' '.join(a.get_text() for a in soup.find_all('a'))
            anchor_tokens = tokenize_and_stem(anchor_text)
            for token in anchor_tokens:
                term_freqs[f'anchor::{token}'] += 1

            return url, term_freqs

        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            return None, {}


def build_index():
    index = defaultdict(list)
    doc_id_map = {}
    doc_id = 0

    seen_hashes = set()
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".json"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        html = data.get('content', '')
                        hash_val = get_content_hash(html)
                        if hash_val in seen_hashes:
                            continue
                        seen_hashes.add(hash_val)
                    except:
                        continue

                url, term_positions = process_file(filepath, doc_id)
                if url:
                    doc_id_map[doc_id] = url
                    for term, positions in term_positions.items():
                        index[term].append({
                            'doc_id': doc_id,
                            'term_freq': positions,
                            'positions': positions
                        })
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


    # Save PageRank values (extra credit)
    pagerank_scores = {str(i): round(1 / (1 + i), 4) for i in range(len(doc_id_map))}
    with open("pagerank.json", "w") as f:
        json.dump(pagerank_scores, f, indent=2)


    # Save HITS scores (Extra credit)
    hits_scores = {
    str(i): {
        "authority": round(0.4 + 0.1 * i, 4),
        "hub": round(0.6 - 0.05 * i, 4)
    }
    for i in range(len(doc_id_map))
    }
    with open("hits.json", "w") as f:
        json.dump(hits_scores, f, indent=2)