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
    def post(self, request, *args, **kwargs):
        # 1. 从请求中获取前端加密的用户名/密码
        encrypted_data = request.data.get('data')

        # 2. 后端解密获取原始凭证
        try:
            decrypted_data = rsa_decrypt(encrypted_data)
            decrypted_data = json.loads(decrypted_data)
            username = decrypted_data.get("username")
            password = decrypted_data.get("password")
            timestamp = decrypted_data.get("timestamp")
            print(f"解密后的用户名: {username}, 密码: {password}, 时间戳: {timestamp}")
        except Exception as e:
            return result.fail('无效的加密数据', code=status.HTTP_400_BAD_REQUEST)

        # 3. 验证用户凭证
        user = authenticate(username=username, password=password)
        if not user:
            return result.fail("用户名或密码错误", code=status.HTTP_401_UNAUTHORIZED)

        # 4. 生成 JWT（使用 simplejwt 的 RefreshToken 类）
        try:
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        except Exception as e:
            return result.fail("生成令牌失败", code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 5. 返回成功响应
        return result.success(response_data)