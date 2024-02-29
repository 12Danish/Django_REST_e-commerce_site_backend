from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from API.mixins import BuyerPermissionMixin, AuthenticationMixin
from API.models import Product
from UserManagement.serializers import UserInfoSerializer
from UserManagement.models import UserInfo
from .models import Cart, OrderHistory
from .mixins import QuerySetForCartMixin, ObjectRetrievalForCartMixin
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


class BuyerListCartItemView(AuthenticationMixin, generics.ListAPIView, QuerySetForCartMixin):
    serializer_class = BuyerCartListSerializer

    '''
    This view is responsible for getting the cart items for authenticated users as well as 
    anonymous users
    '''

    def get_queryset(self):
        return self.get_queryset_by_user(self.request)


class BuyerCartAddItemView(AuthenticationMixin, generics.CreateAPIView):
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
        if Product.objects.filter(id=product_id).exists():
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
                    num_of_items = Cart.objects.filter(buyer=self.request.user).count()


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

            return Response({"error": "adding item to cart unsuccessful"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "No such item exists"}, status=status.HTTP_404_NOT_FOUND)


class BuyerUpdateCartItemView(AuthenticationMixin, ObjectRetrievalForCartMixin, generics.RetrieveUpdateAPIView):
    serializer_class = BuyerProductAddSerializer

    # Performing the update action
    def update(self, request, *args, **kwargs):
        instance = self.handle_object_retrieval()
        logger.info(f"Update view entered {instance}")
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        # Manually update the instance with validated data
        try:
            logger.info(f"This is the instance{instance}")
            if request.user.is_authenticated:
                instance.quantity = serializer.validated_data.get('quantity', instance.quantity)
                instance.save()
            else:
                cart_data = request.session.get('cart_data')
                for item in cart_data:
                    if item['id'] == instance.id:
                        item['quantity'] = serializer.validated_data.get('quantity', item['quantity'])
                        request.session['cart_data'] = cart_data
                        break
                else:
                    return Response({"error": "Item not found in session"}, status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({"error": "Item was not updated in database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "The item was updated successfully"}, status=status.HTTP_200_OK)


class BuyerDeleteCartItemView(AuthenticationMixin, ObjectRetrievalForCartMixin, generics.DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        instance = self.handle_object_retrieval()
        logger.info(f" This is the delete view :{instance}")
        try:
            if request.user.is_authenticated:
                instance.delete()
            else:
                cart_data = request.session.get('cart_data')
                for item in cart_data:
                    if item['id'] == instance.id:
                        cart_data.remove(item)  # Remove the item from cart_data
                        request.session['cart_data'] = cart_data  # Update session with modified cart_data
                        break
                else:
                    return Response({"error": "Item not found in session"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Item was deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as E:
            return Response({"error": f"Delete operation failed with exception {E}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BuyerCheckoutView(AuthenticationMixin, generics.GenericAPIView, QuerySetForCartMixin):
    '''This view will handle the checkout logic.
    It will call another class for sending emails and generating a pdf receipt.
    It will save all the items to the order_history model if the user is authenticated.
    It will delete all the items from the cart.
    '''
    serializer_class = UserInfoSerializer

    def post(self, request, *args, **kwargs):
        cart_items = self.get_queryset_by_user(self.request)
        serializer = self.get_serializer(data=self.request.data)
        # If the cart is non-empty this is run
        if cart_items:
            if serializer.is_valid():
                # Incrementing the n_bought of the product attribute of the item by the qunatity bought
                for item in cart_items:
                    item.product.n_bought += item.quantity
                    item.product.save()

                    # Emptying the cart associated to the user
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
                        cart_items.delete()
                        user_data = UserInfo.objects.filter(user=request.user).first()
                        if not user_data:
                            user_data = UserInfo.objects.create(
                                user=self.request.user,
                                phone_num=serializer.validated_data['phone_num'],
                                address=serializer.validated_data['address'],
                                street=serializer.validated_data['street'],
                                city=serializer.validated_data['city'],
                                neighbourhood=serializer.validated_data['neighbourhood']
                            )
                        BuyerCheckoutView.check_user_info_change(serializer.validated_data, user_data)


                    else:
                        # If the user is not authenticated, clear the cart from the session
                        request.session.pop('cart_data', None)
                return Response({"message": "Order was placed"}, status.HTTP_200_OK)
            else:
                return Response({"error": "User Data in invalid format please follow the required format"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Cart is empty"}, status.HTTP_204_NO_CONTENT)

    @staticmethod
    def check_user_info_change(data, user_data: UserInfo):
        # Check if User model  fields are changed
        if (
                data.get('first_name') != user_data.user.first_name or
                data.get('last_name') != user_data.user.last_name or
                data.get('email') != user_data.user.email
        ):
            user_data.user.first_name = data.get('first_name', user_data.user.first_name)
            user_data.user.last_name = data.get('last_name', user_data.user.last_name)
            user_data.user.email = data.get('email', user_data.user.email)
            user_data.user.save()
        elif (
                data.get('phone_num') != user_data.phone_num or
                data.get('address') != user_data.address or
                data.get('neighbourhood') != user_data.neighbourhood or
                data.get('street') != user_data.street or
                data.get('city') != user_data.city
        ):
            user_data.phone_num = data.get('phone_num')
            user_data.address = data.get('address')
            user_data.city = data.get('city')
            user_data.neighbourhood = data.get('neighbourhood')
            user_data.street = data.get('street')
            user_data.user.save()


class BuyerOrderHistory(AuthenticationMixin, BuyerPermissionMixin, generics.ListAPIView):
    serializer_class = BuyerOrderHistorySerializer

    def get_queryset(self):
        return OrderHistory.objects.filter(buyer=self.request.user)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        if isinstance(exc, PermissionDenied):
            return Response({"detail": "Authentication required for this action."}, status=status.HTTP_401_UNAUTHORIZED)
        return response
