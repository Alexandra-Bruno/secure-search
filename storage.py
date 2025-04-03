import json

index_data = {}

def index_page(url, content):
    index_data[url] = content
    with open('data.json', 'w') as f:
        json.dump(index_data, f)
