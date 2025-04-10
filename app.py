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
    results = set()
    for word in query_words:
        if word in inverted_index:
            if not results:
                results = set(inverted_index[word])
            else:
                results &= set(inverted_index[word])  # Intersection
    print(f"Results: {results}")
    return results


    # Load page data
    with open('data.json', 'r') as f:
        page_data = json.load(f)

    # Prepare display info
    display_results = []
    for url in results:
        title = page_data.get(url, {}).get('title', 'No Title')
        snippet = page_data.get(url, {}).get('snippet', 'No snippet available.')
        display_results.append({
            'url': url,
            'title': title,
            'snippet': snippet
        })

    return display_results
if __name__ == '__main__':
    app.run(debug=True)


