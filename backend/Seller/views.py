from rest_framework import generics
from API.serializers import ProductListSerializer


class SellerProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
