import json

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from ..tasks import *

from api.selfUtils import rsa_decrypt, result

# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
class trigger_task(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            encrypted_data = request.data.get('data')
            decrypted_data = rsa_decrypt(encrypted_data)
            decrypted_data = json.loads(decrypted_data)
            pushToken = decrypted_data.get("pushToken")
            gameToken = decrypted_data.get("gameToken")
            gameId = decrypted_data.get("gameId")
            print(f"解密后的数据: {decrypted_data}")
        except Exception as e:
            return result.fail('无效的加密数据', code=status.HTTP_400_BAD_REQUEST)

        if not gameToken or not gameId:
            return result.fail("缺少参数")
        print("=== 调试 Celery 任务路由 ===")
        print(f"process_data.name = {process_data.name}")
        print(f"process_data.app.main = {process_data.app.main}")
        print(f"process_data.app.conf.task_routes = {process_data.app.conf.task_routes}")
        print("==========================")
        task1 = process_data.delay(gameToken,gameId,pushToken)

        return result.success(f"任务已开始，任务ID{task1.id}")

class playGame(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            encrypted_data = request.data.get('data')
            decrypted_data = rsa_decrypt(encrypted_data)
            decrypted_data = json.loads(decrypted_data)
            pushToken = decrypted_data.get("pushToken")
            gameToken = decrypted_data.get("gameToken")
            gameId = decrypted_data.get("gameId")
            print(f"解密后的数据: {decrypted_data}")
        except Exception as e:
            return result.fail('无效的加密数据', code=status.HTTP_400_BAD_REQUEST)

        if not gameToken or not gameId:
            return result.fail("缺少参数")
        print("=== 调试 Celery 任务路由 ===")
        print(f"play_game.name = {play_game.name}")
        print(f"play_game.app.main = {play_game.app.main}")
        print(f"play_game.app.conf.task_routes = {play_game.app.conf.task_routes}")
        print("==========================")

        task1 = play_game.delay(gameToken, gameId, pushToken)

        return result.success(f"任务已开始，任务ID{task1.id}")