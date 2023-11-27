from rest_framework import authentication
from rest_framework import permissions
from .permissions import IsSellerPermission

# Defining  authentication mixin to be used in all seller views
class SellerAuthenticationMixin():
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]


class SellerPermissionMixin():
    permission_classes = [permissions.IsAuthenticated,IsSellerPermission]
