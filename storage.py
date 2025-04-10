import json

try:
    with open('data.json', 'r') as f:
        index_data = json.load(f)
except FileNotFoundError:
    index_data = {}

def index_page(url, title, snippet):
    index_data[url] = {
        "title": title,
        "snippet": snippet
    }
    with open('data.json', 'w') as f:
        json.dump(index_data, f, indent=4)
