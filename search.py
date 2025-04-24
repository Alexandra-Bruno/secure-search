import json

# Load the inverted index
with open('index.json', 'r') as f:
    inverted_index = json.load(f)

def search(query):
    print(f"Searching for: {query}")
    query_words = query.lower().split()

    with open('index.json', 'r') as f:
        inverted_index = json.load(f)
    
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
        page = page_data.get(url, {})
        display_results.append({
            'url': url,
            'title': page.get('title', 'No Title'),
            'snippet': page.get('snippet', 'No snippet available.')
        })

    print(f"Results: {display_results}")
    return display_results


# Example usage
query = "example search"
print(search(query))
