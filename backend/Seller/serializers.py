from rest_framework import serializers
from API.serializers import ProductSerializer


# This is the special serializer for the seller as the seller and buyer will have different fields to view
class SellerProductSerializer(ProductSerializer):
    pass
