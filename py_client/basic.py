import requests

endpoint = "http://localhost:8000/api/products/"
data = {
    "title": "Fiat Punto",
    "content": "Hot hatch",
    "price": "35000"
}
response = requests.post(endpoint, json=data)
print(response.json())