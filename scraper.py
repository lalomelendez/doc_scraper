import requests
from bs4 import BeautifulSoup
import os
import json
import time
from urllib.parse import urljoin
import logging
from typing import Dict, List
from tqdm import tqdm
import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TailwindDocsScraper:
    def __init__(self, base_url: str = "https://tailwindcss.com/docs", delay: float = 1.0):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.docs_dir = "tailwind_docs"
        os.makedirs(self.docs_dir, exist_ok=True)
        
    def get_all_doc_urls(self) -> List[str]:
        """Get all documentation URLs from the main page."""
        response = self.session.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = []
        
        # Find all navigation links that point to documentation
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/docs/'):
                full_url = urljoin(self.base_url, href)
                if full_url not in urls:
                    urls.append(full_url)
        
        return urls

    def scrape_page(self, url: str) -> Dict:
        """Scrape a single documentation page."""
        try:
            time.sleep(self.delay)
            logger.info(f"Scraping {url}")
            
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            main_content = soup.find('main')
            
            if not main_content:
                logger.warning(f"No main content found for {url}")
                return None
            
            # Remove unwanted elements
            for element in main_content.find_all(['script', 'style', 'nav', 'footer']):
                element.decompose()
            
            # Extract code examples separately
            code_blocks = []
            for code in main_content.find_all('code'):
                code_blocks.append(code.get_text())
                code.decompose()
            
            # Get headers for structure
            headers = []
            for h in main_content.find_all(['h1', 'h2', 'h3']):
                headers.append({
                    'level': int(h.name[1]),
                    'text': h.get_text(strip=True)
                })
            
            return {
                'url': url,
                'title': soup.find('h1').get_text(strip=True) if soup.find('h1') else '',
                'content': main_content.get_text(separator=' ', strip=True),
                'headers': headers,
                'code_examples': code_blocks,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return None

    def scrape_all_docs(self):
        """Scrape all documentation pages and save them."""
        urls = self.get_all_doc_urls()
        documents = []
        
        for url in tqdm(urls, desc="Scraping documentation"):
            doc = self.scrape_page(url)
            if doc:
                documents.append(doc)
                
                # Save individual document
                filename = url.split('/')[-1] or 'index'
                with open(f"{self.docs_dir}/{filename}.json", 'w') as f:
                    json.dump(doc, f, indent=2)
        
        # Save all documents in one file
        with open(f"{self.docs_dir}/all_docs.json", 'w') as f:
            json.dump(documents, f, indent=2)
        
        return documents

class TailwindDocsProcessor:
    def __init__(self, docs_dir: str = "tailwind_docs"):
        self.docs_dir = docs_dir
        self.db_dir = "tailwind_vectordb"
        
        # Explicitly create the vector db directory
        os.makedirs(self.db_dir, exist_ok=True)
        
        self.chunk_size = 500
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        try:
            # Use PersistentClient instead of Client
            self.chroma_client = chromadb.PersistentClient(path=self.db_dir)
            # Try to get existing collection or create new one
            try:
                self.collection = self.chroma_client.get_collection("tailwind_docs")
                logger.info("Found existing collection")
            except:
                self.collection = self.chroma_client.create_collection("tailwind_docs")
                logger.info("Created new collection")
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {str(e)}")
            raise

    def process_docs(self):
        """Process documents and create vector database."""
        docs = self.load_docs()
        all_chunks = []
        
        for doc in tqdm(docs, desc="Processing documents"):
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)
        
        # Create embeddings and add to vector database
        texts = [chunk['text'] for chunk in all_chunks]
        embeddings = self.model.encode(texts)
        
        # Add to Chroma in batches
        batch_size = 500
        for i in tqdm(range(0, len(texts), batch_size), desc="Batches"):
            batch_texts = texts[i:i + batch_size]
            batch_embeddings = embeddings[i:i + batch_size]
            batch_chunks = all_chunks[i:i + batch_size]
            
            self.collection.add(
                embeddings=batch_embeddings.tolist(),
                documents=batch_texts,
                metadatas=[{
                    'url': chunk['url'],
                    'title': chunk['title'],
                    'type': chunk['type']
                } for chunk in batch_chunks],
                ids=[f"chunk_{j}" for j in range(i, i + len(batch_texts))]
            )
        
        # No need to call persist() anymore as PersistentClient handles this automatically

def main():
    # Step 1: Scrape documentation
    scraper = TailwindDocsScraper()
    scraper.scrape_all_docs()
    
    # Step 2: Process and create vector database
    processor = TailwindDocsProcessor()
    processor.process_docs()

if __name__ == "__main__":
    main()