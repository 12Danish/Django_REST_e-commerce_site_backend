from rest_framework import generics
from API.serializers import ProductListSerializer, ProductCreateUpdateSerializer
from API.mixins import AuthenticationMixin
from API.models import Product


# Defining the List View for the seller
# The seller has to be authenticated in order to access this
class SellerProductListView(AuthenticationMixin, generics.ListAPIView):
    serializer_class = ProductListSerializer

    # Getting the queryset
    def get_queryset(self):
        print(self.request.user)
        if self.request.user.groups.filter(name='seller').exists():
            qs = Product.objects.filter(owner=self.request.user)
            return qs
        return Product.objects.none()


class SellerProductCreateView(AuthenticationMixin, generics.CreateAPIView):
    serializer_class = ProductCreateUpdateSerializer
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class SellerProductRUDView(generics.RetrieveUpdateDestroyAPIView):
    pass
