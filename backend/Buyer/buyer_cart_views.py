import uuid
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from API.mixins import BuyerPermissionMixin, AuthenticationMixin
from .models import Cart, OrderHistory
from .mixins import QuerySetForCartMixin
from .serializers import BuyerProductAddSerializer, BuyerOrderHistorySerializer, BuyerCartListSerializer
import logging

# Configuring the django logging to log even the basic things
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
'''
These views need to be modified when the logic for randomly generated system ids for guest users is implemented
'''
'''
Based on the session_id storing the data in the sessions table in the database
storing product_id, quantity in the session model
and performing actions accordingly
the data is deleted once the session expires
when a user logs in and has a valid session the data from it is transferred to the users cart model 


'''


class BuyerListCartItemView(generics.ListAPIView):
    serializer_class = BuyerCartListSerializer
    '''
    This view is responsible for getting the cart items for authenticated users as well as 
    anonymous users
    '''

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(buyer=self.request.user)
        elif self.request.COOKIES.get('sessionid'):
            return self.request.session.get('cart_data')
        else:
            return []


class BuyerCartAddItemView(generics.CreateAPIView):
    '''
    This  view is responsible for both adding a cart_item
    It adds cart Items to the cart model for authenticated users
    Cart items are added to server session for unauthenticated users
    Using djangos middleware a sessionid is stored in a cookie and sent to the browser
    It is then sent with each req till the session expires
    '''
    serializer_class = BuyerProductAddSerializer

    def create(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        post_data_serializer = self.get_serializer(data=request.data)
        if post_data_serializer.is_valid():
            product_data = {'product_id': product_id, 'quantity': post_data_serializer.validated_data['quantity']}
            return_data = {}
            # Handling the case for authenticated users
            if self.request.user.is_authenticated:
                new_item = Cart.objects.create(
                    buyer=self.request.user,
                    **product_data)
                return_data['cart_item_id'] = new_item.id
                num_of_items = enumerate(Cart.objects.filter(buyer=self.request.user))

            # Handling the case for unauthenticated users
            else:
                cart_data = request.session.get('cart_data', [])
                last_id = max([item.get('id', 0) for item in cart_data], default=0)
                new_id = last_id + 1
                product_data['id'] = new_id
                return_data['cart_item_id'] = new_id
                cart_data.append(product_data)
                num_of_items = len(cart_data)
                self.request.session['cart_data'] = cart_data
            return_data['total_items'] = num_of_items
            return Response(
                return_data,
                status=status.HTTP_201_CREATED)

        return Response("Error with adding item to cart", status=status.HTTP_400_BAD_REQUEST)


class BuyerUpdateCartItemView(generics.RetrieveUpdateAPIView, QuerySetForCartMixin):
    serializer_class = BuyerProductAddSerializer

    # Defining the queryset as all items associated to the buyer
    def get_queryset(self):
        return self.get_queryset_by_user(self.request.user, self.request.session.get('device_id'))

    # Getting the object with the id specified from the frontend
    def get_object(self):
        queryset = self.get_queryset()
        return generics.get_object_or_404(queryset, id=self.kwargs.get('pk'))

    # Performing the update action
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        # Manually update the instance with validated data
        instance.quantity = serializer.validated_data.get('quantity', instance.quantity)
        instance.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class BuyerDeleteCartItemView(generics.DestroyAPIView, QuerySetForCartMixin):
    serializer_class = BuyerProductAddSerializer

    def get_queryset(self):
        return self.get_queryset_by_user(self.request.user, self.request.session.get('device_id'))


class BuyerCheckoutView(generics.GenericAPIView, QuerySetForCartMixin):
    '''This view will handle the checkout logic.
    It will call another class for sending emails and generating a pdf receipt.
    It will save all the items to the order_history model if the user is authenticated.
    It will delete all the items from the cart.
    '''

    def get(self, request, *args, **kwargs):
        cart_items = self.get_queryset_by_user(self.request.user, self.request.session.get('device_id'))
        # If the cart is non-empty this is run
        if cart_items:
            # If the user is logged in then saving the bought items to order_history
            if request.user.is_authenticated:
                for item in cart_items:
                    OrderHistory.objects.create(
                        buyer=item.buyer,
                        quantity=item.quantity,
                        product_name=item.product.title,
                        product_image=item.product.image,
                        product_discount=item.product.discount,
                        product_seller=item.product.owner.username
                    )
            # Incrementing the n_bought of the product attribute of the item by the qunatity bought
            for item in cart_items:
                item.product.n_bought += item.quantity
                item.product.save()

            # Emptying the cart associated to the user
            cart_items.delete()
            return Response("Order was placed", status.HTTP_200_OK)
        else:
            return Response("Cart is empty", status.HTTP_204_NO_CONTENT)


class BuyerOrderHistory(AuthenticationMixin, generics.ListAPIView, BuyerPermissionMixin):
    serializer_class = BuyerOrderHistorySerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication required for this action.")
        return OrderHistory.objects.filter(buyer=self.request.user)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        if isinstance(exc, PermissionDenied):
            return Response({"detail": "Authentication required for this action."}, status=status.HTTP_401_UNAUTHORIZED)
        return response
