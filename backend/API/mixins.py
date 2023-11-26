from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer


class ProductQuerySetMixin():
    queryset = Product.objects.all()
