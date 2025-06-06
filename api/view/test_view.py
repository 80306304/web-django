import json

from django.contrib.auth import authenticate
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.function.card import *
from api.selfUtils import rsa_decrypt, result

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class test_f(TokenObtainPairView):
    def get(self, request, *args, **kwargs):
        user = request.user
        # 1. 获取用户的 VIP 到期时间和设备号
        ketList = generate_card_codes(2)
        store_card_codes(ketList,"day")
        # card = Card.objects.filter(status="unused").first()
        # card = model_to_dict(card)
        # 5. 返回成功响应
        return result.success(ketList)