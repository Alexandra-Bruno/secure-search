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
    query_words = query.lower().split()
    results = set()
    for word in query_words:
        if word in inverted_index:
            if not results:
                results = set(inverted_index[word])
            else:
                results &= set(inverted_index[word])  # Intersection
    return results

if __name__ == '__main__':
    app.run(debug=True)
