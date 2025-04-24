import json
import os

def index_page(url, content, title=None, snippet=None):
    data_file = 'data.json'

    # Create the file if it doesn't exist
    if not os.path.exists(data_file):
        with open(data_file, 'w') as f:
            json.dump({}, f)

    # Load existing data
    with open(data_file, 'r') as f:
        data = json.load(f)

    # Update or add new entry
    data[url] = {
        'title': title or 'No Title',
        'snippet': snippet or '',
        'content': content
    }

    # Save back to file
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Indexed: {url}")
