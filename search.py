import json

# Load the inverted index
with open('index.json', 'r') as f:
    inverted_index = json.load(f)

def search(query):
    query_words = query.lower().split()
    results = set()

    for word in query_words:
        if word in inverted_index:
            if not results:
                results = set(inverted_index[word])
            else:
                results &= set(inverted_index[word])  # Intersection of results

    return results

# Example usage
query = "example search"
print(search(query))
