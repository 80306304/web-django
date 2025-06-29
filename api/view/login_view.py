import json

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.function.get_client_ip import get_client_ip
from api.selfUtils import rsa_decrypt, result


class loginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # 1. 从请求中获取前端加密的用户名/密码
        encrypted_data = request.data.get('data')

        # 2. 后端解密获取原始凭证
        try:
            decrypted_data = rsa_decrypt(encrypted_data)
            decrypted_data = json.loads(decrypted_data)
            username = decrypted_data.get("username")
            password = decrypted_data.get("password")
            ip = get_client_ip(request)
            print(f"解密后的数据: {decrypted_data}")
        except Exception as e:
            return result.fail('无效的加密数据', code=status.HTTP_400_BAD_REQUEST)

        # 3. 验证用户凭证
        user = authenticate(username=username, password=password)
        if not user:
            return result.fail("用户名或密码错误", code=status.HTTP_401_UNAUTHORIZED)

        user.login_ip = ip
        user.save()
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