import json
from datetime import time

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from api.function.get_client_ip import get_client_ip
from api.models import CustomUser
from api.selfUtils import rsa_decrypt, result
from api.serializers import UserSerializer
from api.view.regisiter_view import generate_unique_user_code


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

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class getUsers(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.user_level <= 2:
            return result.fail("暂无权限")
        serializer = UserSerializer(CustomUser.objects.all(), many=True)
        return result.success(serializer.data)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class updateUser(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        user = request.user
        encrypted_data = request.data.get('data')
        if user.user_level <= 2:
            return result.fail("暂无权限")

        try:
            decrypted_data = rsa_decrypt(encrypted_data)
            decrypted_data = json.loads(decrypted_data)
            username = decrypted_data.get("username")
            password = decrypted_data.get("password")
            level = decrypted_data.get("level")
            vip_time = decrypted_data.get("vip_time")
            print(f"解密后的数据: {decrypted_data}")
        except Exception as e:
            return result.fail('无效的加密数据', code=status.HTTP_400_BAD_REQUEST)

        findUser = CustomUser.objects.get(username=username)
        findUser.password = password
        if level is not None and level != "":
            if(user.user_level <= level):
                return result.fail("修改失败，权限不足")
            findUser.user_level = int(level)
        if vip_time is not None and vip_time != "":
            findUser.vip_time = time.mktime(time.strptime(vip_time, "%Y-%m-%d %H:%M:%S"))
        findUser.save()
        return result.success("修改成功")


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class addUser(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        user = request.user
        encrypted_data = request.data.get('data')
        if user.user_level <= 2:
            return result.fail("暂无权限")

        try:
            decrypted_data = rsa_decrypt(encrypted_data)
            decrypted_data = json.loads(decrypted_data)
            username = decrypted_data.get("username")
            email = decrypted_data.get("email")
            password = decrypted_data.get("password")
            level = decrypted_data.get("level")
            vip_time = decrypted_data.get("vip_time")
            print(f"解密后的数据: {decrypted_data}")
        except Exception as e:
            return result.fail('无效的加密数据', code=status.HTTP_400_BAD_REQUEST)
        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'invited_parent': user.user_code,
            'user_code': generate_unique_user_code()
        }
        # 可选参数处理
        if level is not None:
            user_data['user_level'] = level
        if vip_time is not None:
            user_data['vip_time'] = vip_time
        addUser = CustomUser.objects.create_user(**user_data)
        addUser.save()
        return result.success("添加成功")