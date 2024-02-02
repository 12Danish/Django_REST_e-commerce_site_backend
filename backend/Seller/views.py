from rest_framework import generics
from API.product_serializers import ProductListSerializer, ProductCreateSerializer, ProductDetailSerializer
from API.mixins import AuthenticationMixin, SellerPermissionMixin
from API.models import Product

'''
The seller has to be authenticated in order to access the seller views
'''


# Defining the List View for the seller
class SellerProductListView(AuthenticationMixin, SellerPermissionMixin, generics.ListAPIView):
    serializer_class = ProductListSerializer

    # Getting the queryset
    def get_queryset(self):
        print(self.request.user)
        if self.request.user.groups.filter(name='seller').exists():
            return Product.objects.filter(owner=self.request.user)
        return Product.objects.none()


# This is the view for creating a product
class SellerProductCreateView(AuthenticationMixin, SellerPermissionMixin, generics.CreateAPIView):
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


# This view handles the logic for retrieving, updating and deleting products
class SellerProductRUDView(generics.RetrieveUpdateDestroyAPIView, AuthenticationMixin, SellerPermissionMixin):
    serializer_class = ProductDetailSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)
