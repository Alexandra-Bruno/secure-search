# crawler.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from storage import index_page  # Saves title and snippet

def crawler(start_url, visited=None, depth=2):
    if visited is None:
        visited = set()

    if depth == 0 or start_url in visited:
        return

    visited.add(start_url)

    try:
        response = requests.get(start_url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else 'No Title'
        text = soup.get_text(separator=' ', strip=True)
        snippet = ' '.join(text.split()[:50])  # First 50 words

        print(f'Visited URL: {start_url} - Title: {title}')

        # Save full content to data.json
        index_page(start_url, text)

        for link in soup.find_all('a', href=True):
            next_url = urljoin(start_url, link['href'])
            crawler(next_url, visited, depth - 1)

    except requests.RequestException as e:
        print(f'Failed to fetch {start_url}: {e}')
