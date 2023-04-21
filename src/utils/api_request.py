import requests

def get(url: str):
    response = requests.get(url)
    return response

def post(url: str, data: dict):
    response = requests.post(url, json=data)
    return response

def get_dict(url: str):
    try:
        resp = get(url)
        return resp.json(), resp.status_code
    except Exception as e:
        print('error while get api call')
        print(e)
    return None, None

def post_dict(url: str, data: dict):
    try:
        resp = post(url, data)
        return resp.json(), resp.status_code
    except Exception as e:
        print('error while post api call')    
        print(e)
    return None, None