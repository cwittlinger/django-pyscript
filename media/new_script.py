import requests

def fetch_api(url: str):
    response = requests.get(url)
    print(response.json() )

_CALLABLE = fetch_api