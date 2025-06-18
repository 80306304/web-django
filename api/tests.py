import json
from selfUtils import rsa_decrypt,rsa_encrypt



def crypt():
    param = {
        "username":"liyx1",
        "password":"liyx1",
        "email":"111@qq.com",
        "card":"FFFCCCB5BCCD4AA0824E34C75D1A9475"
    }
    param = {
        "count":"3",
        "type":"week"
    }
    param = {
        "key":"2B20636F02B24E41A0E0E657B5B0E91A"
    }
    paramstr = json.dumps(param)
    data = rsa_encrypt(paramstr)
    print(data)
    raw = rsa_decrypt(data)
    raw_json = json.loads(raw)
    print(raw_json)



if __name__ == '__main__':
    crypt()