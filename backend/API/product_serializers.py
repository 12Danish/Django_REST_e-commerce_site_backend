from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateTimeField
from rest_framework.utils.serializer_helpers import ReturnDict

from .models import Product
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.reverse import reverse
from .review_serializers import ReviewSerializer
from .user_serializers import PublicUserSerializer


class ProductListSerializer(serializers.ModelSerializer):
    '''
     This is the serializer for the products model which is being used for listing data
    '''

    # Defining this attribute which will produce the url for the detail view
    detail_url = serializers.SerializerMethodField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    date_created = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'price',
            'image',
            'sale_item',
            'sale_price',
            'category',
            'date_created',
            'detail_url'

        ]

    @staticmethod
    def get_date_created(obj):
        return ProductDetailSerializer.get_date_created(obj)

    # Getting the url based on the user who is logged in
    def get_detail_url(self, obj: Product) -> reverse:
        # Getting the request
        request = self.context.get('request')
        # Seeing if the user is a seller
        if request.user.groups.filter(name='seller').exists():
            return reverse("Seller:product-retrieve", kwargs={"pk": obj.pk}, request=request)
        else:
            return reverse("Buyer:product-retrieve", kwargs={"pk": obj.pk}, request=request)


# This serializer will handle serialization for the Detail View
class ProductDetailSerializer(serializers.ModelSerializer):
    '''
         This is the serializer for the products model which is being used for displaying dtailed data
         for a particular product

        '''

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    reviews = serializers.SerializerMethodField(read_only=True)
    seller = PublicUserSerializer(source="owner", read_only=True)
    date_created = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product

        fields = [
            'id',
            'title',
            'price',
            'image',
            'category',
            'discount',
            'sale_price',
            'seller',
            'description',
            'date_created',
            'reviews'
        ]

    @staticmethod
    def get_date_created(obj: Product) -> DateTimeField:
        return obj.date_created.strftime("%Y-%m-%d")

    @staticmethod
    def get_reviews(obj: Product) -> ReturnDict:
        reviews = obj.review.all()
        return ReviewSerializer(reviews, many=True).data


# This serializer will handle the serialization for creating a new product
class ProductCreateSerializer(serializers.ModelSerializer):
    '''
        This serializer is primarily being used for converting the data of the new product entered
        by the seller and saving it to the database
        '''

    # Having a validator to ensure that each product name is unique
    title = serializers.CharField(max_length=200)
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Product

        fields = [
            'id',
            'title',
            'image',
            'price',
            'description',
            'discount',
            'category'
        ]

    def validate(self, attrs, *args, **kwargs):
        if attrs.get('price') < 0 or (attrs.get('discount') and attrs.get('discount') < 0):
            raise ValidationError
        request = self.context.get('request')

        # Dynamically setting the queryset of the UniqueValidator based on the request user
        if request and request.user:
            self.fields['title'].validators.append(
                UniqueValidator(
                    queryset=Product.objects.filter(owner=request.user),
                    message='Product with this title already exists for this user.'
                )
            )
        else:
            # Fallback if request or request.user is not provided
            raise ValueError('Request or user not provided.')

        return attrs
