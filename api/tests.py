import json
from selfUtils import rsa_decrypt,rsa_encrypt



def crypt():
    param = {
        "password":"liyx1111",
        "email":"111111@qq.com",
        
        "invite_code":"12345678"
    }
    param = { "username": "liyx", "password": "liyx" }
    # param = {
    #     "count":"3",
    #     "type":"week"
    # }
    # param = {
    #     "key":"A53A19BB32894995A30BDBE80C2BFA39"
    # }
    paramstr = json.dumps(param)
    data = rsa_encrypt(paramstr)
    print(data)
    raw = rsa_decrypt(data)
    raw_json = json.loads(raw)
    print(raw_json)



if __name__ == '__main__':
    crypt()