import json

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.selfUtils import rsa_decrypt, result

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class varifyVip(TokenObtainPairView):
    def get(self, request, *args, **kwargs):
        user = request.user
        # 1. 获取用户的 VIP 到期时间和设备号
        vip_time = user.vip_time
        device = user.device
        ip_address = user.ip_address
        data = {
            'vip_time': vip_time,
            'device': device,
            'ip_address': ip_address
        }
        # 5. 返回成功响应
        return result.success(data)