from rest_framework import serializers
from API.product_serializers import ProductListSerializer


class BuyerProductSerializer(serializers.Serializer):
    '''
    This serializer will be used to store both the order history and the cart Data
    '''
    cart_item_id = serializers.PrimaryKeyRelatedField(source='id', read_only=True)
    buyer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    quantity = serializers.IntegerField()
    product_detail = ProductListSerializer(source='product', read_only=True)
