import uuid

from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from API.permissions import IsBuyerPermission
from API.mixins import BuyerPermissionMixin, AuthenticationMixin
from .models import Cart, OrderHistory
from .mixins import QuerySetForCartMixin
from .serializers import BuyerProductAddSerializer, BuyerOrderHistorySerializer, BuyerCartListSerializer

'''
These views need to be modified when the logic for randomly generated system ids for guest users is implemented
'''


class BuyerListCartItemView(generics.ListAPIView, QuerySetForCartMixin):
    serializer_class = BuyerCartListSerializer

    def get_queryset(self):
        return self.get_queryset_by_user(self.request.user, self.request.session['device_id'])


class BuyerCartAddItemView(generics.CreateAPIView, QuerySetForCartMixin):
    '''
    This  view is responsible for both adding a cart_item and displaying users cart
    '''
    serializer_class = BuyerProductAddSerializer

    def create(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product_data = {'product_id': product_id, 'quantity': serializer.validated_data['quantity']}
            if self.request.user.is_authenticated:
                Cart.objects.create(
                    buyer=self.request.user,
                    **product_data)

            elif not request.session['device_id'].exists():
                device_id = uuid.uuid4()
                Cart.objects.create(device_id=device_id, **product_data)
                self.request.session['device_id'] = device_id

            return Response(f"Item was successfully added to cart {product_id} {serializer.data}",
                            status=status.HTTP_201_CREATED)

        return Response("Error with adding item to cart", status=status.HTTP_400_BAD_REQUEST)


class BuyerUpdateCartItemView(generics.RetrieveUpdateAPIView, QuerySetForCartMixin):
    serializer_class = BuyerProductAddSerializer

    # Defining the queryset as all items associated to the buyer
    def get_queryset(self):
        return self.get_queryset_by_user(self.request.user, self.request.session['device_id'])

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
        return self.get_queryset_by_user(self.request.user, self.request.session['device_id'])


class BuyerCheckoutView(generics.GenericAPIView,QuerySetForCartMixin):
    '''This view will handle the checkout logic.
    It will call another class for sending emails and generating a pdf receipt.
    It will save all the items to the order_history model if the user is authenticated.
    It will delete all the items from the cart.
    '''

    def get(self, request, *args, **kwargs):
        cart_items = self.get_queryset_by_user(self.request.user, self.request.session['device_id'])
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
