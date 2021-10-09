import requests
import json
import random

url = f"https://api.henrikdev.xyz/valorant/v1/website/en-us?filter=game_updates"

r = requests.get(url)

data = json.loads(r.text)
data = data['data']
i = 0

while not "Patch Notes" in data[i]['title']:
        i += 1

print(data[i]['title'])

url = f"https://api.henrikdev.xyz/valorant/v1/website/en-us"

r = requests.get(url)

data = json.loads(r.text)
data = data['data']
i = random.randint(0, len(data))

print(data[i]['banner_url'])