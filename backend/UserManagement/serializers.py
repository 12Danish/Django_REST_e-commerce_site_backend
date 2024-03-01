from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    is_seller = serializers.BooleanField()
    is_buyer = serializers.BooleanField()

    # Making sure user can register as seller or buyer but not both
    def validate(self, attrs):
        is_seller = attrs.get('is_seller')
        is_buyer = attrs.get('is_buyer')

        if is_buyer is True and is_seller is True:
            raise serializers.ValidationError("Either 'is_buyer' or 'is_seller' should be true, not both.")

        return attrs


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    is_seller = serializers.BooleanField()
    is_buyer = serializers.BooleanField()


class UserInfoSerializer(serializers.Serializer):
    '''
    This serialzer is used within the checkout view of the buyer
    '''
    first_name = serializers.CharField(max_length=1000)
    last_name = serializers.CharField(max_length=1000)
    email = serializers.EmailField()
    phone_num = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=1000)
    street = serializers.CharField(max_length=100, allow_null=True, allow_blank=True, required=False)
    neighbourhood = serializers.CharField(max_length=1500)
    city = serializers.CharField(max_length=1000)
