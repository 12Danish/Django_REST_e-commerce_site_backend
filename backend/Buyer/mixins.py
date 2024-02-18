from .models import Cart


class QuerySetForCartMixin:
    @staticmethod
    def get_queryset_by_user(request):
        if request.user.is_authenticated:
            return Cart.objects.filter(buyer=request.user)
        elif request.COOKIES.get('sessionid'):
            return request.session.get['cart_data']
        else:
            return []

