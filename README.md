# Search Engine — Milestone 1 (Information Analyst)

This project builds an inverted index from a collection of crawled UCI web pages.

## Files

- `main.py`: Builds the inverted index
- `utils.py`: Tokenization and stemming helpers
- `index.json`: (Generated) The final inverted index
- `doc_ids.json`: (Generated) Maps doc_id → URL
- `report.txt`: (Generated) Contains index analytics

## How to Run

1. Install dependencies:

pip3 install beautifulsoup4 nltk


2. Run the script
python3 main.py

3. Outputs:
- `index.json`
- `doc_ids.json`
- `report.txt`


## Ignored Files
Files like `index.json`, `doc_ids.json`, and `__pycache__/` are ignored in `.gitignore`

---