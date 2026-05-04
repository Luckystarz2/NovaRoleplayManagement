import requests

def send_webhook(url, message):
    data = {
        "content": message
    }
    requests.post(url, json=data)