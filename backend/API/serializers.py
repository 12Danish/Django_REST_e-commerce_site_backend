from .models import Product
from rest_framework import serializers


# This is the serializer for the products model
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price'
        ]
