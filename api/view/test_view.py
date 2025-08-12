import json

from django.contrib.auth import authenticate
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from api.function.card import *
from api.selfUtils import rsa_decrypt, result

# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
class test_f(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # 将请求的正文部分转换为响应
        record = json.loads(request.body.decode('utf-8'))
        record = json.dumps(record,indent=4)
        print(record)
        return Response(record)