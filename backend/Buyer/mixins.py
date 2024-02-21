from django.db.models import Q, QuerySet
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Cart
import logging

# Configuring the django logging to log even the basic things
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class QuerySetForCartMixin:
    '''
    This mixin is responsible for retrieving the queryset for both authenticated users as well as
    anonymous users
    It converts the anonymous users into Queryset objects before returning
    '''

    def get_queryset_by_user(self, request):
        if request.user.is_authenticated:
            return Cart.objects.filter(buyer=request.user)
        elif request.COOKIES.get('sessionid'):
            cart_data = request.session.get('cart_data')
            if cart_data:
                logger.info(cart_data)
                return self.convert_session_cart_to_cart_model_instances(cart_data)

        return Cart.objects.none()

    @staticmethod
    def convert_session_cart_to_cart_model_instances(session_cart_data):
        logger.info(session_cart_data)
        queryset = []  # An empty queryset to start with
        for cart_item_data in session_cart_data:
            cart_item = Cart(**cart_item_data)
            logger.info(queryset)
            queryset.append(cart_item)
        logger.info(queryset)
        return queryset


class ObjectRetrievalForCartMixin(QuerySetForCartMixin):
    """
    This class is responsible for retrieving the object from the Cart model in the db
    or from th session
    """
    def handle_object_retrieval(self):
        return self.get_object()

    def get_queryset(self):
        return self.get_queryset_by_user(self.request)

        # Getting the object with the id specified from the frontend
    def get_object(self):
        queryset = self.get_queryset()
        logger.info(f"Update view{queryset} {self.kwargs.get('pk')}")
        if isinstance(queryset, QuerySet):
            # If queryset is a Django QuerySet, use get_object_or_404
            return generics.get_object_or_404(queryset, id=self.kwargs.get('pk'))
        # If it is a list of model instances doing this
        else:
            for product in queryset:
                if product.id == self.kwargs.get('pk'):
                    return product

        return Response({"detail": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
