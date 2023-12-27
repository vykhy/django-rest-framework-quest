import requests

endpoint = "http://localhost:8000/api/products/"

data = {
    "title": "New Generic Product",
    "price" :11.99
}
response = requests.post(endpoint, json=data)
print(response.json())