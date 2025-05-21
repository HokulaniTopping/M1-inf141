import json
import os
from utils import tokenize_and_stem
import math

# constants
INDEX_PATH = "index.json"
DOC_IDS_PATH = "doc_ids.json"

class SearchEngine:
    def __init__(self, index_path=INDEX_PATH, doc_ids_path=DOC_IDS_PATH):
        """Initialize the search engine by loading the index and document ID map."""
        self.load_index(index_path)
        self.load_doc_ids(doc_ids_path)
        self.total_docs = len(self.doc_id_map)



    def load_index(self, path):
        """Load the inverted index from a JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            self.index = json.load(f)
        
    def load_doc_ids(self, path):
        """Load the document ID to URL mapping from a JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            self.doc_id_map = json.load(f)
        
    def search(self, query, top_n=5):
        """
        Search for documents that match the query (boolean AND).
        
        Args:
            query (str): The search query.
            top_n (int): The number of top results to return.
            
        Returns:
            list: A list of (url, score) tuples for the top matching documents.
        """
        # tokenize and stem the query
        query_terms = tokenize_and_stem(query)
        
        if not query_terms:
            return []
        
        # for AND queries, find documents that contain all query terms
        doc_scores = self._boolean_and_search(query_terms)

        # convert the document scores to a list of (url, score) tuples
        results = [(self.doc_id_map.get(str(doc_id)), score) 
                  for doc_id, score in doc_scores]
        
        return results[:top_n]

    def _boolean_and_search(self, query_terms):
        """
        Perform a boolean AND search using the query terms.
        
        Args:
            query_terms (list): The tokenized and stemmed query terms.
            
        Returns:
            list: A list of (doc_id, score) tuples for documents that match all query terms.
        """
        # find documents that contain the first query term
        if not query_terms or query_terms[0] not in self.index:
            return []
            
        # Get the documents that contain the first term
        candidate_docs = {posting["doc_id"]: posting["term_freq"] 
                         for posting in self.index[query_terms[0]]}
        
        # for each remaining term, filter the candidate documents
        for term in query_terms[1:]:
            print("THIS IS THE TOKENIZED AND STEMMED TERM "+term)
            if term not in self.index:
                return []  # no documents contain this term
                
            # get the documents that contain this term
            term_docs = {posting["doc_id"]: posting["term_freq"] 
                        for posting in self.index[term]}
            
            # keep only the documents that contain both the current term and all previous terms
            common_docs = {}
            for doc_id in candidate_docs:
                if doc_id in term_docs:
                    # USING TF IDF SCORING I HOPE I DID THIS RIGHT
                    common_docs[doc_id] = candidate_docs[doc_id] + self.compute_tf_idf(term, doc_id)
            
            candidate_docs = common_docs

        # convert the dictionary to a list of (doc_id, score) tuples and sort by score
        doc_scores = [(doc_id, score) for doc_id, score in candidate_docs.items()]
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        #sorted by score
        
        return doc_scores
        

    def compute_tf_idf(self, term, doc_id):
        # Get term frequecy in doc
        postings = self.index.get(term, [])
        tf = 0
        df = len(postings)
        
        for posting in postings:
            if posting["doc_id"] == doc_id:
                tf = posting["term_freq"]
                break

        if df == 0 or tf == 0:
            return 0

        # Calculate IDF
        idf = math.log(self.total_docs / (1 + df))
        
        return tf * idf

    def create_report(self, queries, top_n=5, output_file="search_report.txt"):
        print("ABOUT TO CREATE FILE")
        """Create a report of the top results for each query."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Search Engine Report - Milestone 2\n")
            f.write("=================================\n\n")
            
            for query in queries:
                f.write(f"Query: {query}\n")
                f.write("Top Results:\n")
                
                results = self.search(query, top_n)
                
                for i, (url, score) in enumerate(results, 1):
                    f.write(f"{i}. {url} (Score: {score})\n")
                
                f.write("\n")
            
            f.write("End of Report\n")

# simple command-line interface
def cli():
    search_engine = SearchEngine()
    
    print("Search Engine CLI (type 'q' to quit)")
    print("====================================")

    queries_run = []
    
    while True:
        query = input("\nEnter a search query: ")
        
        if query.lower() == 'q':
            break
            
        queries_run.append(query)
        results = search_engine.search(query)
        
        print("\nSearch Results:")
        if not results:
            print("No results found.")
        else:
            for i, (url, score) in enumerate(results, 1):
                print(f"{i}. {url} (Score: {score})")


    if queries_run:
        search_engine.create_report(queries_run)
        print("Search report saved as search_report.txt")





# test with the specified queries
def test_queries():
    search_engine = SearchEngine()
    queries = [
        "cristina lopes",
        "machine learning",
        "ACM",
        "master of software engineering"
    ]
    
    print("Bout to create report")
    search_engine.create_report(queries)
    
    print("Report created: search_report.txt")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_queries()
    else:
        cli()

