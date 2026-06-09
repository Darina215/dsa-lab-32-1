import requests

response = requests.post(
    "http://127.0.0.1:5000/set",
    json={
        "key": "name",
        "value": "Иван"
    }
)

print(response.json())

import requests

response = requests.get(
    "http://127.0.0.1:5000/get/name"
)

print(response.json())

import requests

response = requests.get(
    "http://127.0.0.1:5000/exists/name"
)

print(response.json())

import requests

response = requests.delete(
    "http://127.0.0.1:5000/delete/name"
)

print(response.json())



