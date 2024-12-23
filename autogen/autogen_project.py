import requests

url = "https://api.hyperbolic.xyz/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJldXJ5dGhtaWEuaW50ZXJhY3RpdmVAZ21haWwuY29tIiwiaWF0IjoxNzMzNTA1NzcxfQ.NXnZfydBvo1K6SeB-N7x47CngdjfzcvjpuldaR_3tWY"
}

agents = ["Agent 1", "Agent 2", "Agent 3", "Agent 4", "Agent 5"]
conversation = []

for round in range(3):
    for agent in agents:
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": f"What do you think about React and Tailwind, {agent}?"
                }
            ],
            "model": "meta-llama/Llama-3.3-70B-Instruct",
            "max_tokens": 128,
            "temperature": 0.1,
            "top_p": 0.9
        }
        response = requests.post(url, headers=headers, json=data)
        conversation.append((agent, response.json()["choices"][0]["message"]["content"]))

for agent, message in conversation:
    print(f"{agent}: {message}")
