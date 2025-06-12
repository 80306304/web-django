import json
from selfUtils import rsa_decrypt,rsa_encrypt



def crypt():
    param = {
        "username":"liyx",
        "password":"liyx"
    }
    param = {
        "count":"1",
        "type":"hour"
    }
    param = {
        "key":"0D1ADC70F5C0400089B7127D6B0FCDB4"
    }
    paramstr = json.dumps(param)
    data = rsa_encrypt(paramstr)
    print(data)
    raw = rsa_decrypt(data)
    raw_json = json.loads(raw)
    print(raw_json)



if __name__ == '__main__':
    crypt()