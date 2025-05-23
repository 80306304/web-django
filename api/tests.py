import json


from selfUtils import rsa_decrypt,rsa_encrypt



def crypt():
    username = 'liyx'
    password = 'liyx'
    param = {
        "username":username,
        "password":password
    }
    paramstr = json.dumps(param)
    data = rsa_encrypt(paramstr)
    print(data)
    raw = rsa_decrypt(data)
    raw_json = json.loads(raw)
    print(raw_json)


if __name__ == '__main__':
    crypt()