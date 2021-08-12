import requests
import json

url = "https://api.thecatapi.com/v1/images/search?format=json"

payload={}
files={}
headers = {
  'Content-Type': 'application/json',
  'x-api-key': '17d94b92-754f-46eb-99a0-65be65b5d18f'
}

response = requests.request("GET", url, headers=headers, data=payload, files=files)
loaded = json.loads(response.text)

print(response.text)

