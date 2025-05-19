import ast
import json

from django.test import TestCase
from selfUtils import *
# Create your tests here.
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

username = 'liyx'
password = 'liyx'
param = {
    "username":username,
    "password":password
}
paramstr = json.dumps(param)

if __name__ == '__main__':
    data = rsa_encrypt(paramstr)
    print(data)
    raw = rsa_decrypt(data)
    raw_json = json.loads(raw)
    print(raw_json.get("username"))




