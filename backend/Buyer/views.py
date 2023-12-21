from rest_framework import generics
from API.product_serializers import ProductListSerializer, ProductDetailSerializer
from API.mixins import BuyerPermissionMixin
from API.review_serializers import ReviewSerializer
from API.models import Product, Review
from datetime import timedelta
from django.utils import timezone


# A simple function to display only the appropriate products within a time field
def one_month_ago():
    time = timezone.now() - timedelta(days=30)
    return time


# This view handles sending the data over to the front end to display the lists
class BuyerProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    min_time = one_month_ago()

    # This will define the queryset for the display for the buyer
    def get_queryset(self):
        # Getting all the objects from the
        qs = Product.objects.filter(date_created__gte=self.min_time)
        # Checking if a category has been defined by the user in the params
        category = self.request.query_params.get('category', None)
        # If user has specified the category then getting only the items of that category
        if category:
            qs = qs.filter(category=category)
            return qs
        qs = [product for product in qs if product.popular]
        return qs


# This view is responsible for retrieving the desired product
class BuyerProductRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"


class BuyerPostReviewView(BuyerPermissionMixin, generics.CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_serializer_context(self):
        # Include product_id in the serializer context
        context = super().get_serializer_context()
        context['product_id'] = self.kwargs.get('pk')
        return context

