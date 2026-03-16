import requests
import json

# 1. Update the URL to Groq's completion endpoint
url = "https://api.groq.com/openai/v1/chat/completions"

# 2. Update the Payload
# Note: Changed "model" to a valid Groq model name like 'llama-3.3-70b-versatile'
payload = json.dumps({
  "model": "llama-3.3-70b-versatile", 
  "messages": [
    {
      "role": "system",
      "content": "You are an expert coding assistant specializing in writing clean, efficient, and production-ready code..." # Your full system prompt here
    },
    {
      "role": "user",
      "content": "write a e-commerce simple program to buys and sell products in python. Create a single file."
    }
  ],
  "max_tokens": 2000, # Increased as per your system prompt request
  "temperature": 0.3
})

# 3. Update Headers to include your API Key
# Replace 'gsk_yOuRApiKeyHeRe' with your actual key from console.groq.com
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer gsk_yOuRApiKeyHeRe'
}

# Send the request
response = requests.request("POST", url, headers=headers, data=payload)

# Check for errors and print the response
if response.status_code == 200:
    print(response.json()['choices'][0]['message']['content'])
else:
    print(f"Error {response.status_code}: {response.text}")