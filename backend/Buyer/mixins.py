from .models import Cart


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
            return self.convert_session_cart_to_query_set(cart_data)
        else:
            Cart.objects.none()

    @staticmethod
    def convert_session_cart_to_query_set(session_cart_data):
        queryset = Cart.objects.none()  # An empty queryset to start with
        for cart_item_data in session_cart_data:
            cart_item = Cart(**cart_item_data)
            queryset |= Cart.objects.filter(id=cart_item.id)  # Add each item to the queryset
        return queryset
