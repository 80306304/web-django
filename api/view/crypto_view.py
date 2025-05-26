import json

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from DjangoProject1.settings import RSA_PUBLIC_KEY, RSA_PRIVATE_KEY

from api.selfUtils import rsa_decrypt, result

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class varifyVip(TokenObtainPairView):
    def get(self, request, *args, **kwargs):
        user = request.user
        # 1. 获取用户的 VIP 到期时间和设备号

        data = {
            "type":"RSA",
            "RSA_PUBLIC_KEY":RSA_PUBLIC_KEY,
            "RSA_PRIVATE_KEY":RSA_PRIVATE_KEY
        }
        if power == 0:return result.success(data)
        data = {
            'vip_time': vip_time,
            'device': device,
            'regisiter_ip': regisiterIp,
            'login_ip': loginIp,
            'power': power
        }
        # 5. 返回成功响应
        return result.success(data)