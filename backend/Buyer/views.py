from rest_framework import generics, status
from API.product_serializers import ProductListSerializer, ProductDetailSerializer
from API.mixins import BuyerPermissionMixin
from API.review_serializers import ReviewSerializer
from API.models import Product, Review
from rest_framework.response import Response

from .models import Cart
from .serializers import BuyerProductSerializer
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


class BuyerListCartAddItemView(generics.ListCreateAPIView):
    '''
    This  view is responsible for both adding a cart_item and displaying users cart
    '''
    serializer_class = BuyerProductSerializer

    # Returning only those items associated with the end user
    def get_queryset(self):
        return Cart.objects.filter(buyer=self.request.user)

    # The create method  here is necessary as my serializer is not associated to one specific model
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request, 'product_id': kwargs.get('pk')})
        if serializer.is_valid():
            Cart.objects.create(product_id=serializer.validated_data['product_id'],
                                buyer=serializer.validated_data['buyer'],
                                quantity=serializer.validated_data['quantity'])
            return Response(f"Item was successfully added to cart {serializer.data}",
                            status=status.HTTP_201_CREATED)

        return Response("Error with adding item to cart", status=status.HTTP_400_BAD_REQUEST)


class BuyerDeleteCartItemView(generics.DestroyAPIView):
    pass


class CheckoutView:
    pass
