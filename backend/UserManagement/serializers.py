from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    is_seller = serializers.BooleanField(default=False)
    is_buyer = serializers.BooleanField(default=True)

    # Making sure user can register as seller or buyer but not both
    def validate(self, attrs):
        is_seller = attrs.get('is_seller')
        is_buyer = attrs.get('is_buyer')

        if is_buyer and is_seller:
            raise serializers.ValidationError("Either 'is_buyer' or 'is_seller' should be true, not both.")

        return attrs


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    is_seller = serializers.BooleanField(default=False)
    is_buyer = serializers.BooleanField(default=True)
