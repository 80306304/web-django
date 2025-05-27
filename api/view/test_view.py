import json

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.function.card import generate_card_codes
from api.selfUtils import rsa_decrypt, result


class test_f(TokenObtainPairView):
    def get(self, request, *args, **kwargs):
        user = request.user
        # 1. 获取用户的 VIP 到期时间和设备号
        str = generate_card_codes(1)
        # 5. 返回成功响应
        return result.success(str)