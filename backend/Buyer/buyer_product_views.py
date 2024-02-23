from rest_framework import generics
from API.product_serializers import ProductListSerializer, ProductDetailSerializer
from API.mixins import BuyerPermissionMixin
from API.review_serializers import ReviewSerializer
from API.models import Product, Review
from API.mixins import AuthenticationMixin
from API.permissions import IsBuyerPermission
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
        # Getting all the objects from the
        qs = Product.objects.latest()
        # Checking if a category has been defined by the user in the params
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        popular = self.request.query_params.get('popular')
        logger.debug(f'Initial queryset: {qs}')
        # If user has specified the category then getting only the items of that category
        if category:
            qs = Product.objects.category(category)
        elif search:
            qs = Product.objects.search(search, self.request.user)
        elif popular:
            qs = Product.objects.popular()

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
