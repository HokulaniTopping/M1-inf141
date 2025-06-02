import json
import os
from utils import tokenize_and_stem
import math
from collections import defaultdict
import time
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
        
    def search(self, query, top_n=100):
        """
        Search for documents that match the query.
        
        Args:
            query (str): The search query.
            top_n (int): The number of top results to return.
            
        Returns:
            list: A list of (url, score) tuples for the top matching documents.
        """
        start_time = time.time()

        # tokenize and stem the query
        query_terms = tokenize_and_stem(query)
        
        if not query_terms:
            return []
        
        #find documents that contain all query terms
        doc_scores = self._tf_idf_search(query_terms)

        # convert the document scores to a list of (url, score) tuples
        elapsed_time = time.time() - start_time
        results = [(self.doc_id_map.get(str(doc_id)), score) 
                  for doc_id, score in doc_scores]
        
        end_time = time.time() - start_time
        print("ELAPSED TIME: ", end_time)

        return results[:top_n], end_time


    def _tf_idf_search(self, query_terms):
        scores = defaultdict(float)
        doc_freqs = {}
        doc_norms = defaultdict(float)
        query_vector = defaultdict(float)
        query_norm = 0

        # IDF per term
        for term in query_terms:
            postings = self.index.get(term, [])
            doc_freqs[term] = len(postings)
            idf = math.log(self.total_docs / (1 + len(postings)))
            query_vector[term] = idf  # query is binary TF, so just use IDF
            query_norm += idf ** 2

            #cosine similarity (extra credit)
            for posting in postings:
                doc_id = posting["doc_id"]
                tf_idf = posting["term_freq"] * idf
                scores[doc_id] += tf_idf * query_vector[term]
                doc_norms[doc_id] += tf_idf ** 2

        query_norm = math.sqrt(query_norm)

        for doc_id in scores:
            doc_norm = math.sqrt(doc_norms[doc_id])
            if doc_norm != 0 and query_norm != 0:
                scores[doc_id] /= (doc_norm * query_norm)
            else:
                scores[doc_id] = 0

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)


    # def _tf_idf_search(self, query_terms):
    #     scores = defaultdict(float)
    #     doc_freqs = {}
        
    #     # calculate IDF for each query term
    #     for term in query_terms:
    #         postings = self.index.get(term, [])
    #         doc_freqs[term] = len(postings)

    #     for term in query_terms:
    #         postings = self.index.get(term, [])
    #         idf = math.log(self.total_docs / (1 + doc_freqs[term]))
    #         for posting in postings:
    #             doc_id = posting["doc_id"]
    #             tf = posting["term_freq"]
    #             scores[doc_id] += tf * idf

    #     return sorted(scores.items(), key=lambda x: x[1], reverse=True)
        

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
        results, elapsed = search_engine.search(query)
        print(f"\nSearch Results (took {elapsed:.4f} seconds):")
        
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


