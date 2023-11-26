from rest_framework import generics
from rest_framework import generics
from API.mixins import ProductQuerySetMixin
from .serializers import BuyerProductSerializer


class SellerProductListView(ProductQuerySetMixin,generics.ListAPIView):
    serializer_class = BuyerProductSerializer
