from rest_framework import serializers
from API.product_serializers import ProductListSerializer


class BuyerProductSerializer(serializers.Serializer):
    '''
    This serializer will be used to store both the order history and the cart Data
    '''
    buyer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    quantity = serializers.IntegerField()
    product_id = serializers.IntegerField()
    product_detail = ProductListSerializer(source='product', read_only=True)
