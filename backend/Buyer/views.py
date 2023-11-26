from rest_framework import generics
from API.serializers import ProductListSerializer
from API.models import Product
from datetime import timedelta
from django.utils import timezone


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


class BuyerProductRetrieveView(generics.RetrieveAPIView):
    pass
