import requests

url = "https://api.hyperbolic.xyz/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJldXJ5dGhtaWEuaW50ZXJhY3RpdmVAZ21haWwuY29tIiwiaWF0IjoxNzMzNTA1NzcxfQ.NXnZfydBvo1K6SeB-N7x47CngdjfzcvjpuldaR_3tWY"
}
data = {
    "messages": [
        {
            "role": "user",
            "content": "What can I do in LA?"
        }
    ],
    "model": "meta-llama/Llama-3.3-70B-Instruct",
    "max_tokens": 512,
    "temperature": 0.1,
    "top_p": 0.9
}

response = requests.post(url, headers=headers, json=data)
print(response.text)
