import requests
import json


url = "https://api.nasa.gov/planetary/apod"

payload={}
files={}
headers = {
'Content-Type': 'application/json',
'x-api-key': "oTVGiGXsY9BBZnvkTcBctUlXM8s61CMiCPfI8pVe"
}

response = requests.request("GET", url, headers=headers, data=payload, files=files)

print(json.loads(response.text))
