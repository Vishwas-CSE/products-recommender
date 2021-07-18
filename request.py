import requests


def send():
    params = {'user':'rick'}
    response = requests.post(url="http://localhost:5000/recommend", params=params)
    print(response.status_code)

send()