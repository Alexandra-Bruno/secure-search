# This code should consist of a web crawler/spider.
# The purpose of a web crawler is to search the web and download pages.
# Code: Python
# Coder: Alexandra Bruno

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from Index import save_to_index 

def crawler(start_url, visited=None, depth=2):
    # Initialize the visited page set.
    # This ensures the same page isn't visited twice.
    if visited is None:
        visited = set()

    # The variable 'depth' limits how deep the crawler will go.
    if depth == 0:
        return

    # Check if the URL has already been visited.
    if start_url in visited:
        return

    visited.add(start_url)

    try:
        # Send a GET request to the URL and limit wait time to 5 sec to preserve efficiency/resources.
        response = requests.get(start_url, timeout=5)
        response.raise_for_status() # Raise and exception for bad responses.

        # Parse the webpage content using BeautifulSoup.
        soup = BeautifulSoup(response.text, 'html.parser')

        # Print the page title if available.
        page_title = soup.title.string if soup.title else 'No title found!'
        print(f'Visited URL: {start_url} - Title: {page_title}')

        #Save URL and extracted text content
        save_to_index(start_url, soup.get_text())  
        
        # Locate and follow all links on the page
        for link in soup.find_all('a', href=True):
            next_url = urljoin(start_url, link['href']) # Convert relative URLs to real URLs (what's typed by a user VS something that works).
            crawler(next_url, visited, depth - 1)

    # Handle potential network errors.
    except requests.RequestException as e:
        print(f'Failed to fetch {start_url}: {e}')

