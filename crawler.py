# crawler.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from storage import index_page  # Saves title and snippet

# Create a requests session with no cookies!
session = requests.Session()
session.cookies.clear()

def crawler(start_url, visited=None, depth=2):
    if visited is None:
        visited = set()

    # The variable 'depth' limits how deep the crawler will go.
    if depth == 0 or start_url in visited:
        return

    visited.add(start_url)

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; SecureBot/1.0)",
            "DNT": "1" # A polite request not to be tracked.
        }
        
        # Send a GET request to the URL and limit wait time to 5 sec to preserve efficiency/resources. 
        # Disable cookies by sending an empty cookie jar
        response = session.get(start_url, headers=headers, cookies={}, timeout=5)
        response.raise_for_status() # Raise and exception for bad responses.

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
