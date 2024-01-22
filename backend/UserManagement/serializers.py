from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    is_seller = serializers.BooleanField(default=False)
    is_buyer = serializers.BooleanField(default=True)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    is_seller = serializers.BooleanField(default=False)
    is_buyer = serializers.BooleanField(default=True)


