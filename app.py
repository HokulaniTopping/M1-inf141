from flask import Flask, request, render_template_string
from search_engine import SearchEngine

app = Flask(__name__)
search_engine = SearchEngine()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Search Engine - Milestone 2</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        .search-container {
            margin: 20px 0;
        }
        input[type="text"] {
            width: 70%;
            padding: 10px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4285f4;
            color: white;
            border: none;
            cursor: pointer;
        }
        .result {
            margin: 20px 0;
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        .result a {
            color: #1a0dab;
            text-decoration: none;
            font-size: 18px;
        }
        .result a:hover {
            text-decoration: underline;
        }
        .result .url {
            color: #006621;
            font-size: 14px;
            margin: 5px 0;
        }
        .result .score {
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>Search Engine - Milestone 2</h1>
    
    <div class="search-container">
        <form action="/" method="get">
            <input type="text" name="query" value="{{ query }}" placeholder="Enter search query">
            <button type="submit">Search</button>
        </form>
    </div>
    
    {% if query %}
        <h2>Results for "{{ query }}"</h2>
        
        {% if results %}
            {% for url, score in results %}
                <div class="result">
                    <a href="{{ url }}" target="_blank">{{ url.split('/')[-1] if '/' in url else url }}</a>
                    <div class="url">{{ url }}</div>
                    <div class="score">Score: {{ score }}</div>
                </div>
            {% endfor %}
        {% else %}
            <p>No results found.</p>
        {% endif %}
    {% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    query = request.args.get('query', '')
    results = []
    
    if query:
        results = search_engine.search(query)
    
    return render_template_string(HTML_TEMPLATE, query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)