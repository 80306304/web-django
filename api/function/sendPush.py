import requests
import json

def sendMsg(token,title,content):
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    res = requests.post(url, data=body, headers=headers)
    return res.json()