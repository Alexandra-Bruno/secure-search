from flask import Flask, request, render_template, jsonify
import json

app = Flask(__name__)

@app.after_request
def disable_caching(response):
    response.headers["Cache-Control"] = "no-store"
    return response



# Load the inverted index once
with open('index.json', 'r') as f:
    inverted_index = json.load(f)

# Load the site data once (optional: move this to a function if you update it often)
with open('data.json', 'r') as f:
    page_data = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = search(query)
    return render_template('index.html', results=results)

@app.route('/suggest')
def suggest():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])

    suggestions = []
    for url, data in page_data.items():
        title = data.get('title', '').lower()
        if query in title:
            suggestions.append(data.get('title', ''))
        if len(suggestions) >= 5:
            break

    return jsonify(suggestions)

def search(query):
    print(f"Searching for: {query}")
    query_words = query.lower().split()

    result_urls = set()
    for word in query_words:
        if word in inverted_index:
            if not result_urls:
                result_urls = set(inverted_index[word])
            else:
                result_urls &= set(inverted_index[word])  # intersection

    display_results = []
    for url in result_urls:
        title = page_data.get(url, {}).get('title', 'No Title')
        snippet = page_data.get(url, {}).get('snippet', 'No snippet available.')
        display_results.append({
            'url': url,
            'title': title,
            'snippet': snippet
        })

    print(f"Results: {display_results}")
    return display_results

if __name__ == '__main__':
    app.run(debug=True)

print("Running on http://127.0.0.1:5000/")

