import requests


def url_shortener(link,url_api = "http://localhost:8000/shorten"):
    payload = {"url":link}
    try:
        response = requests.post(url_api,json=payload)
        response.raise_for_status()
        data=response.json()
        return data['short_url']
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None