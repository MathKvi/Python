import requests

url = "http://localhost:5000/hundar"

response = requests.get(url)

info = response.json()

print(info)