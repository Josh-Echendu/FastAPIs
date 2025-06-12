import requests

endpoint = "http://127.0.0.1:8000/posts"

data = {
    "title": "top beaches in Africa",
    "content": "check out these awesome African Beaches",
    "published": True
}

get_response = requests.post(endpoint, json=data)

print(get_response.text)
# print(get_response.headers)
print(get_response.status_code)