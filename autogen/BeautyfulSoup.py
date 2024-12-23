import requests
from bs4 import BeautifulSoup
import os
import json

# Scrape Tailwind docs
base_url = "https://tailwindcss.com/docs"
# You'll need to implement crawling logic here to get all doc pages

def scrape_docs(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as err:
        print("Error fetching page:", err)
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract relevant content
    # Remove navigation, headers, etc.
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get the main content
    main_content = soup.find('main')
    
    # Check if main_content is not None
    if main_content is not None:
        # Remove any unnecessary elements
        for element in main_content.find_all(['nav', 'header', 'footer']):
            element.decompose()
        
        # Extract the text from the main content
        content = main_content.get_text()
    else:
        content = soup.get_text()
    
    return content

def scrape_all_docs():
    all_content = ""
    pages = []
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/docs/'):
            pages.append('https://tailwindcss.com' + href)
    for page in pages:
        all_content += scrape_docs(page) + "\n"
    return all_content

if __name__ == "__main__":
    print(scrape_all_docs())
