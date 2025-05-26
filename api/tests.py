import json

from api.function.card import generate_card_codes
from selfUtils import rsa_decrypt,rsa_encrypt



def crypt():
    username = 'liyx'
    password = 'liyx'
    param = {
        "email":"test111",
        "password":"test111"
    }
    paramstr = json.dumps(param)
    data = rsa_encrypt(paramstr)
    print(data)
    raw = rsa_decrypt(data)
    raw_json = json.loads(raw)
    print(raw_json)


if __name__ == '__main__':
    # crypt()
    generate_card_codes(1)