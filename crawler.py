import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from storage import index_page  # Must handle title/snippet/content

# Create a requests session with no cookies
session = requests.Session()
session.cookies.clear()

headers = {
            "User-Agent": "Mozilla/5.0 (compatible; SecureBot/1.0)",
            "DNT": "1"
        }

def crawler(start_url, visited, depth=1):
    if depth == 0 or start_url in visited:
        return

    visited.add(start_url)

    try:
        response = session.get(start_url, headers=headers, cookies={}, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        #Get basic Information
        title = soup.title.string.strip() if soup.title else 'No Title'
        text = soup.get_text(separator=' ', strip=True)
        snippet = ' '.join(text.split()[:50])  # First 50 words

        # Save full content to data.json
        index_page(start_url, text, title=title, snippet=snippet)

        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('#') or href.startswith('mailto:'):
                continue  # Skip internal anchors and email links
            next_url = urljoin(start_url, href)
            time.sleep(1)  # Be polite — 1 second delay
            crawler(next_url, visited, depth - 1)

    except requests.RequestException as e:
        print(f'Failed to fetch {start_url}: {e}')


seeds = [
    
    # Universities with mostly static, text-based homepages
    "https://www.morgan.edu/",

    "https://www.mit.edu/",
    "https://www.stanford.edu/",
    "https://www.cmu.edu/",

    
    # Blogs and publications
    "https://blog.mozilla.org/en/",
    "https://www.dictionary.com",

    # Educational or scientific orgs
    "https://www.nasa.gov/",
    "https://www.cdc.gov/",
    
]

# Global visited set shared across all seed calls
visited = set()
for seed in seeds:
    crawler(seed, visited=set(), depth=1)
