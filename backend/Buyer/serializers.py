from django.db.models import PositiveIntegerField
from rest_framework import serializers
from API.product_serializers import ProductListSerializer
from .models import OrderHistory


class BuyerProductSerializer(serializers.Serializer):
    '''
    This serializer will be used to store both the order history and the cart Data
    '''
    cart_item_id = serializers.PrimaryKeyRelatedField(source='id', read_only=True)
    buyer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    quantity = serializers.IntegerField()
    product_detail = ProductListSerializer(source='product', read_only=True)


class BuyerOrderHistorySerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderHistory

        fields = [
            'product_name',
            'product_seller',
            'price',
            'product_image',
            'quantity',
            'buyer',
            'purchased_at'
        ]

    def get_price(self, obj: OrderHistory) -> PositiveIntegerField or None:
        if obj.product_discount and obj.product_price is not None:
            return obj.product_price - (obj.product_price * (obj.product_discount / 100))
        return obj.product_price
