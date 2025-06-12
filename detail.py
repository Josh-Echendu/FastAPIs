import requests

endpoint = "http://127.0.0.1:8000/posts/20"


get_response = requests.get(endpoint)

# print(get_response.json()['detail'])
print(get_response.text)
print(get_response.status_code)