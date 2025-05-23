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
        regisiterIp = user.regisiter_ip
        loginIp = user.login_ip
        power = user.user_level
        data = {
            'msg': "账号已被封禁",
            'power': power
        }
        if power == 0:return result.fail(data)
        data = {
            'vip_time': vip_time,
            'device': device,
            'regisiter_ip': regisiterIp,
            'login_ip': loginIp,
            'power': power
        }
        # 5. 返回成功响应
        return result.success(data)