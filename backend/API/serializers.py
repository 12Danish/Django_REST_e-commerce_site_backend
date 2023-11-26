from .models import Product
from rest_framework import serializers


# This is the serializer for the products model
class ProductListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField

    class Meta:
        model = Product
        fields = [
            'title',
            'price',
            'sale_price',
            'popular'
        ]

    def get_detail_url(self, obj, ):
        request = self.context.get('request')
        pass


class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

    fields = [
        'title',
        'price',
        'sale_price',
        'popular',
        'owner',
        'description',
        'date_created',

    ]
