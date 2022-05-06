import json
import requests


url = "https://rickies.co/api/chairmen.json"

headers = {'accept': 'application/json'}
r = requests.get(url, headers=headers)
john = json.loads(r.text)

print(john)