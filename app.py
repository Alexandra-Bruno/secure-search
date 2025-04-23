from flask import Flask, request, render_template
import json

app = Flask(__name__)

# Load the inverted index
with open('index.json', 'r') as f:
    inverted_index = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = search(query)
    return render_template('index.html', results=results)

def search(query):
    print(f"Searching for: {query}")
    query_words = query.lower().split()

    with open('data.json', 'r') as f:
        page_data = json.load(f)

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
