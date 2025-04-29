from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

word_bank = set()

# Blocks any untrusted JavaScript or other extenral hacking
@app.after_request
def disable_caching(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' https:; style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;"
    return response


def duckduckgo_search(query):
    search_url = "https://html.duckduckgo.com/html/"
    payload = {
        'q': query
    }

    try:
        response = requests.post(search_url, data=payload, timeout=7)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        links = soup.find_all('a', attrs={'class': 'result__a'}, limit=10)

        for link in links:
            title = link.get_text()
            url = link.get('href')

            # Find snippet (from nearby div if possible)
            snippet_div = link.find_parent('div', class_='result__body')
            snippet = snippet_div.get_text(separator=' ', strip=True) if snippet_div else ''

            results.append({
                'url': url,
                'title': title,
                'snippet': snippet
            })

            words_in_title = title.lower().split()
            words_in_snippet = snippet.lower().split()

            for word in words_in_title + words_in_snippet:
                clean_word = ''.join(char for char in word if char.isalnum())
                if len(clean_word) > 2:
                    word_bank.add(clean_word)

        return results

    except Exception as e:
        print(f"Error searching DuckDuckGo: {e}")
        return []


@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = duckduckgo_search(query)
    return render_template('index.html', results=results)

@app.route('/suggest')
def suggest():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])

    matches = [word for word in word_bank if word.startswith(query)]
    return jsonify(matches[:5])


if __name__ == '__main__':
    app.run(debug=True)

print("Running on http://127.0.0.1:5000/")
