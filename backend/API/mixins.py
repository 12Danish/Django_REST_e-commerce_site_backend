from rest_framework import authentication
from rest_framework import permissions
from .permissions import IsSellerPermission, IsBuyerPermission
from rest_framework_simplejwt.authentication import JWTAuthentication


# Defining  authentication mixin to be used in all seller views
class AuthenticationMixin:
    '''
    This mixin just has the authentication classes defined which are being used in different views
               '''
    authentication_classes = [JWTAuthentication]


class SellerPermissionMixin:
    '''
        This mixin just has the permission classes defined which are being used in different views for the seller
                   '''
    permission_classes = [permissions.IsAuthenticated, IsSellerPermission]


class BuyerPermissionMixin:
    '''
            This mixin just has the permission classes defined which are being used in some views for the buyer
                       '''
    permission_classes = [permissions.IsAuthenticated, IsBuyerPermission]
