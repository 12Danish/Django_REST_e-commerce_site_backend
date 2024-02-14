from .models import Cart


class QuerySetForCartMixin:
    @staticmethod
    def get_queryset_by_user(buyer, device_id=None):
        if buyer.is_authenticated:
            return Cart.objects.filter(buyer=buyer)
        else:
            return Cart.objects.filter(device_id=device_id)
