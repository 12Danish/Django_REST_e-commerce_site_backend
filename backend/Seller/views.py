from django.core.exceptions import MultipleObjectsReturned
from rest_framework import generics
from API.product_serializers import ProductListSerializer, ProductCreateSerializer, ProductDetailSerializer
from API.mixins import AuthenticationMixin, SellerPermissionMixin
from API.models import Product
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
import logging

# Configuring the django logging to log even the basic things
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

'''
The seller has to be authenticated in order to access the seller views
'''


# Defining the List View for the seller
class SellerProductListView(AuthenticationMixin, SellerPermissionMixin, generics.ListAPIView):
    serializer_class = ProductListSerializer

    # Getting the queryset
    def get_queryset(self):
        logger.info(self.request.user)
        return Product.objects.filter(owner=self.request.user)


# This is the view for creating a product
class SellerProductCreateView(AuthenticationMixin, SellerPermissionMixin, generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.all()
    parser_classes = FormParser, MultiPartParser, JSONParser

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


# This view handles the logic for retrieving, updating and deleting products
class SellerProductRUDView(AuthenticationMixin, SellerPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    parser_classes = FormParser, MultiPartParser, JSONParser

    def get_queryset(self):
        logger.info(self.request.user)
        return Product.objects.filter(id=self.kwargs.get('pk'), owner=self.request.user)
