from .models import Product
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


# This is the serializer for the products model
class ProductListSerializer(serializers.ModelSerializer):
    # Defining this attribute which will produce the url for the detail view
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


# This serializer will handle serialization for the Detail View
class ProductDetailSerializer(serializers.ModelSerializer):
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


# This serializer will handle the serialization for creating a new product
class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200, validators=[UniqueValidator(queryset=Product.objects.all())])

    class Meta:
        model = Product

        fields = [
            'title',
            'price',
            'description',
            'discount',
        ]
