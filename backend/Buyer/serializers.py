from django.db.models import PositiveIntegerField
from rest_framework import serializers
from API.models import Product
from .models import OrderHistory, Cart


class BuyerProductAddSerializer(serializers.Serializer):
    '''
    This serializer will be used to store both the order history and the cart Data
    '''
    quantity = serializers.IntegerField(write_only=True)


class BuyerCartListSerializer(serializers.Serializer):
    cart_item_id = serializers.SerializerMethodField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    product_detail = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_cart_item_id(obj):
        if isinstance(obj, Cart):
            return obj.id
        elif isinstance(obj, dict):
            return obj['id']
        return None

    @staticmethod
    def get_product_detail(obj):
        product = None
        if isinstance(obj, Cart):
            product = obj.product
        elif isinstance(obj, dict):
            product = Product.objects.filter(id=obj['product_id']).first()
        return {
            "title": product.title,
            "price": product.sale_price
        }


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
