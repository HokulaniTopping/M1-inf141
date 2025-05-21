import os
from search_engine import SearchEngine

def generate_report():
    """
    Generate a report with the top 5 URLs
    for each of the required queries.
    """
    search_engine = SearchEngine()
    queries = [
        "cristina lopes",
        "machine learning",
        "ACM",
        "master of software engineering"
    ]
    
    # create a report with the top 5 URLs for each query
    search_engine.create_report(queries, top_n=5, output_file="m2_report.txt")
    
    # print the report contents
    with open("m2_report.txt", "r") as f:
        print(f.read())
    
    print("Report saved to m2_report.txt")

if __name__ == "__main__":
    generate_report()