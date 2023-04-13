import requests

def get(url: str):
    response = requests.get(url)
    return response

def post(url: str, data: dict):
    response = requests.post(url, data=data)
    return response

def get_dict(url: str):
    resp = get(url)
    return resp.json(), resp.status_code

def post_dict(url: str, data: dict):
    resp = post(url, data)
    return resp.json(), resp.status_code