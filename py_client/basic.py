import requests

endpoint = "http://localhost:8000/api/"

response = requests.get(endpoint, params={"search": "Jhon"}, json={"name": "John"})
print(response.json())