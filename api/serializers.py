# myapp/serializers.py
from rest_framework import serializers
from .models import Card, CustomUser


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'  # 返回所有字段，也可以指定 ['id', 'name', 'description'] 等
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','last_login','user_level','is_active','date_joined']  # 返回所有字段，也可以指定 ['id', 'name', 'description'] 等
