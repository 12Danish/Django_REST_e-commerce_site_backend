from rest_framework import authentication
from rest_framework import permissions
from .permissions import IsSellerPermission, IsBuyerPermission


# Defining  authentication mixin to be used in all seller views
class AuthenticationMixin():
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]


class SellerPermissionMixin():
    permission_classes = [permissions.IsAuthenticated, IsSellerPermission]


class BuyerPermissionMixin():
    permission_classes = [permissions.IsAuthenticated, IsBuyerPermission]
