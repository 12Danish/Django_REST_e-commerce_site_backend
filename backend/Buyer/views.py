from rest_framework import generics
from API.product_serializers import ProductListSerializer, ProductDetailSerializer
from API.mixins import BuyerPermissionMixin
from API.review_serializers import ReviewSerializer
from API.models import Product, Review
from datetime import timedelta
import logging
from django.utils import timezone

# Configuring the django logging to log even the basic things
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# This view handles sending the data over to the front end to display the lists


class BuyerProductListView(generics.ListAPIView):
    '''
    This view is handling listing out the products for the buyer.
    By default it only returns the popular products unless specifed otherwise
    '''
    serializer_class = ProductListSerializer

    # This will define the queryset for the display for the buyer
    def get_queryset(self):
        # Getting all the objects from the
        qs = Product.objects.filter(date_created__gte=self.one_month_ago())
        # Checking if a category has been defined by the user in the params
        category = self.request.query_params.get('category', None)
        logger.debug(f'Initial queryset: {qs}')
        # If user has specified the category then getting only the items of that category
        if category:
            qs = qs.filter(category=category)
            return qs
        qs = [product for product in qs if product.popular]
        logger.debug(f'Final queryset: {qs}')
        return qs

        # A simple function to display only the appropriate products within a time field

    def one_month_ago(self):
        time = timezone.now() - timedelta(days=60)
        return time


# This view is responsible for retrieving the desired product
class BuyerProductRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"


class BuyerPostReviewView(BuyerPermissionMixin, generics.CreateAPIView):
    '''
    This vieww is responsible for saving the review posted by the buyer to the review model.
    It requires permission as defined in the BuyerPermissionMixin.
    It is adding the id of the product to the context for the serializer
    '''
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_serializer_context(self):
        # Include product_id in the serializer context
        context = super().get_serializer_context()
        context['product_id'] = self.kwargs.get('pk')
        return context


class BuyerAddCartItemView(generics.CreateAPIView):
    pass


class BuyerDeleteCartItemView(generics.DestroyAPIView):
    pass


class CheckoutView:
    pass
