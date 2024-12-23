import chromadb
from typing import List, Dict
import autogen
import json
import requests
from typing import Callable

class TailwindDocsHelper:
    def __init__(self, db_dir: str = "tailwind_vectordb"):
        self.chroma_client = chromadb.PersistentClient(path=db_dir)
        try:
            self.collection = self.chroma_client.get_collection("tailwind_docs")
        except:
            raise ValueError("Collection 'tailwind_docs' not found. Please run scraper.py first.")
    
    def search_docs(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search the vector database for relevant documentation."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
        
        return formatted_results

def create_tailwind_agent():
    """Create an AutoGen agent with access to Tailwind documentation."""
    docs_helper = TailwindDocsHelper()
    
    config_list = [{
        "model": "meta-llama/Llama-3.3-70B-Instruct",
        "base_url": "https://api.hyperbolic.xyz/v1",
        "api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJldXJ5dGhtaWEuaW50ZXJhY3RpdmVAZ21haWwuY29tIiwiaWF0IjoxNzMzNTA1NzcxfQ.NXnZfydBvo1K6SeB-N7x47CngdjfzcvjpuldaR_3tWY"
    }]

    llm_config = {
        "config_list": config_list,
        "temperature": 0.1,
        "max_tokens": 512,
        "top_p": 0.9,
    }

    # Create the agent
    agent = autogen.AssistantAgent(
        name="tailwind_expert",
        llm_config=llm_config,
        system_message="""You are a Tailwind CSS expert assistant. 
        Use the function search_tailwind_docs to find relevant documentation when needed.
        Always reference specific Tailwind classes and provide clear explanations.""",
        function_map={
            "search_tailwind_docs": docs_helper.search_docs
        }
    )
    
    return agent