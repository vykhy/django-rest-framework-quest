import requests

endpoint = "http://localhost:8000/api/"

response = requests.post(endpoint, json={"title": "Best Book", "price": 12.99})
print(response.json())