from rest_framework import generics
from API.product_serializers import ProductListSerializer, ProductCreateSerializer, ProductDetailSerializer
from API.mixins import SellerAuthenticationMixin, SellerPermissionMixin
from API.models import Product

'''
The seller has to be authenticated in order to access the seller views
'''


# Defining the List View for the seller
class SellerProductListView(SellerAuthenticationMixin, SellerPermissionMixin, generics.ListAPIView):
    serializer_class = ProductListSerializer

    # Getting the queryset
    def get_queryset(self):
        print(self.request.user)
        if self.request.user.groups.filter(name='seller').exists():
            qs = Product.objects.filter(owner=self.request.user)
            return qs
        return Product.objects.none()


# This is the view for creating a product
class SellerProductCreateView(SellerAuthenticationMixin, SellerPermissionMixin, generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


# This view handles the logic for retrieving, updating and deleting products
class SellerProductRUDView(generics.RetrieveUpdateDestroyAPIView, SellerAuthenticationMixin, SellerPermissionMixin, ):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"
