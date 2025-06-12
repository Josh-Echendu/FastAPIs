import requests

endpoint = "http://127.0.0.1:8000/posts/50"

data = {
    'title': "joshua ik",
    'content': "josh love",
    'published': False,
}

get_response = requests.put(endpoint, json=data)

# print(get_response.json()['detail'])
print(get_response.text)
print(get_response.status_code)