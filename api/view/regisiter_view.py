import json
import random

from django.contrib.auth import authenticate
from django.core.validators import validate_email
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.function.card import use_card
from api.function.get_client_ip import get_client_ip
from api.models import CustomUser
from api.selfUtils import rsa_decrypt, result
from django.core.exceptions import ObjectDoesNotExist

class regisiterView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # 1. 从请求中获取前端加密的用户名/密码
        encrypted_data = request.data.get('data')

        # 2. 后端解密获取原始凭证
        try:
            decrypted_data = json.loads(rsa_decrypt(encrypted_data))

            email = decrypted_data.get("email")
            password = decrypted_data.get("password")
            invite_code = decrypted_data.get("invite_code")
            card_code = decrypted_data.get("card_code")
            ip = get_client_ip(request)
            print(f"解密后的数据 {decrypted_data}")
        except Exception as e:
            return result.fail('无效的加密数据', code=status.HTTP_400_BAD_REQUEST)
        # 邮箱格式验证
        try:
            validate_email(email)
        except Exception:
            return result.fail('邮箱格式不正确')

        if CustomUser.objects.filter(username=email).exists():
            return result.fail('用户已被注册')
        if CustomUser.objects.filter(email=email).exists():
            return result.fail('用户已被注册')

        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            invited_parent=invite_code,
            regisiter_ip=ip,
            user_code=generate_unique_user_code()
        )
        user.save()

        try:
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            if card_code != "" and card_code is not None:
                print(card_code)
                res = use_card(card_code, user)
                data = res.data
                response_data["auth"] = data
            return result.success(response_data)

        except Exception as e:
            return result.fail("生成令牌失败", code=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generate_unique_user_code():
    """生成唯一的8位数字用户编码"""
    while True:
        # 生成8位随机数字字符串
        code = ''.join(random.choices('0123456789', k=8))
        try:
            # 检查是否已存在
            CustomUser.objects.get(user_code=code)
        except ObjectDoesNotExist:
            # 不存在，返回该编码
            return code
        # 如果存在，继续循环