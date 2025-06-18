import json

from django.contrib.auth import authenticate
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.function.card import *
from api.selfUtils import rsa_decrypt, result

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class createCard(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        user = request.user
        power = user.user_level
        if power <= 2: return result.success("无权限")

        encrypted_data = request.data.get('data')
        try:
            decrypted_data = rsa_decrypt(encrypted_data)
            decrypted_data = json.loads(decrypted_data)
            count = int(decrypted_data.get("count"))
            type = decrypted_data.get("type")
            print(f"解密后的值{decrypted_data}")
        except Exception as e:
            return result.fail('无效的加密数据', code=status.HTTP_400_BAD_REQUEST)

        if(count <= 0):result.fail('最少生成一张卡密')

        ketList = generate_card_codes(count)
        store_card_codes(ketList,type)

        return result.success(ketList)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class useCard(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        user = request.user
        power = user.user_level
        if power <= 2: return result.success("无权限")

        encrypted_data = request.data.get('data')
        try:
            decrypted_data = rsa_decrypt(encrypted_data)
            decrypted_data = json.loads(decrypted_data)
            key = decrypted_data.get("key")
            print(f"解密后的值{decrypted_data}")
        except Exception as e:
            return result.fail('无效的加密数据', code=status.HTTP_400_BAD_REQUEST)
        res = use_card(key, user)
        return res