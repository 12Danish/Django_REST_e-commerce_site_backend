from rest_framework.permissions import DjangoModelPermissions


# It is necessary to be a seller to have permssion to the seller views
class IsSellerPermission(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        if request.user.groups.filter(name='seller').exists():
            return True
        return False

    # Checking if the user is signed in as a buyer


class IsBuyerPermission(DjangoModelPermissions):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='buyer').exists():
            return True
        return False
