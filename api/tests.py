import json
from selfUtils import rsa_decrypt,rsa_encrypt



def crypt():
    param = {
        "email":"",
        "password":"",
        "invite_code":"",
        "card_code":""
    }
    param = { "username": "liyx", "password": "lyx121216" }

    # param = {
    #     "count":"3",
    #     "type":"week"
    # }
    param = {
        "key":"A6881C1EC560493C96C4E266F6D5ACEE"
    }
    paramstr = json.dumps(param)
    data = rsa_encrypt(paramstr)
    print(data)
    raw = rsa_decrypt(data)
    raw_json = json.loads(raw)
    print(raw_json)



if __name__ == '__main__':
    crypt()