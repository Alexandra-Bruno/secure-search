import json
import nltk
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

# Inverted index format: {"word": ["url1", "url2", ...]}
inverted_index = defaultdict(set)

# Load stored pages
with open('data.json', 'r') as f:
    index_data = json.load(f)

# Preprocessing and indexing
stop_words = set(stopwords.words('english'))

def build_index():
    nltk.download('stopwords')
    nltk.download('punkt')

    for url, data in index_data.items():
        content = data if isinstance(data, str) else data.get("content", "")
        words = word_tokenize(content.lower())
        for word in words:
            if word.isalnum() and word not in stop_words:
                inverted_index[word].add(url)

    with open('index.json', 'w') as f:
        json.dump({k: list(v) for k, v in inverted_index.items()}, f)

# Build the index
build_index()
