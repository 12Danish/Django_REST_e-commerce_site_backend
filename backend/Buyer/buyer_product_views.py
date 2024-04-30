import pdb

from rest_framework import generics
from API.product_serializers import ProductListSerializer, ProductDetailSerializer
from API.mixins import BuyerPermissionMixin
from API.review_serializers import ReviewSerializer
from API.models import Product, Review
from API.mixins import AuthenticationMixin
import logging

# Configuring the django logging to log even the basic things
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# This view handles sending the data over to the front end to display the lists


class BuyerProductListView(generics.ListAPIView):
    '''
    This view is handling listing out the products for the buyer.
    By default it only returns the Latest products unless specifed otherwise
    It handles the search as well
    '''
    serializer_class = ProductListSerializer

    # This will define the queryset for the display for the buyer
    def get_queryset(self):
        # Getting all the latest objects from the db
        qs = Product.objects.latest()
        # Checking if a category has been defined by the user in the params
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        popular = self.request.query_params.get('popular')
        sale = self.request.query_params.get('sale')

        logger.debug(f'Initial queryset: {qs}')
        # If user has specified the category then getting only the items of that category
        if category:
            qs = Product.objects.category(category)
        elif search:
            qs = Product.objects.search(search, self.request.user)
        elif popular:
            qs = Product.objects.popular()
        elif sale:
            qs = Product.objects.sale_items()

        qs = self.product_specifications(qs)
        return qs

    def product_specifications(self, qs):
        order_by = self.request.query_params.get('order_by')
        order = self.request.query_params.get('order')
        filter_type = self.request.query_params.get('filter_type')
        filter_amount = self.request.query_params.get('filter_amount')

        if filter_type and filter_amount:
            qs = qs.price_filter(filter_type, filter_amount)

        if order_by and order_by.lower() == 'price':
            logger.info("Attempting to order by price")

            qs = qs.order_by_price(order)
        elif order_by and order_by.lower() == "date":
            qs = qs.order_by_date(order)

        return qs


# This view is responsible for retrieving the desired product
class BuyerProductRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"


class BuyerPostReviewView(AuthenticationMixin, BuyerPermissionMixin, generics.CreateAPIView):
    '''
    This view is responsible for saving the review posted by the buyer to the review model.
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
