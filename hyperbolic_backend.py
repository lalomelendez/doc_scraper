import requests
from typing import Dict, List, Optional, Union
from autogen.oai.completion import Completion

class HyperbolicCompletion(Completion):
    def create(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[Dict, List[Dict]]:
        """Create completion using Hyperbolic API."""
        
        url = "https://api.hyperbolic.xyz/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJldXJ5dGhtaWEuaW50ZXJhY3RpdmVAZ21haWwuY29tIiwiaWF0IjoxNzMzNTA1NzcxfQ.NXnZfydBvo1K6SeB-N7x47CngdjfzcvjpuldaR_3tWY"
        }
        
        data = {
            "messages": messages,
            "model": model or "meta-llama/Llama-3.3-70B-Instruct",
            "max_tokens": max_tokens or 512,
            "temperature": temperature or 0.1,
            "top_p": top_p or 0.9,
        }
        
        response = requests.post(url, headers=headers, json=data)
        return response.json()