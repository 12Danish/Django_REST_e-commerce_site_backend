from rest_framework.permissions import DjangoModelPermissions


class IsSellerPermission(DjangoModelPermissions):
    '''
        This class inherits the djangoModelPermission in order to add custom view permission for the seller
        Also it looks for the seller group within created user
        '''

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
    '''
           This class inherits the DjangoModelPermission in order to add custom permission for the buyer
           Also it looks for the buyer group within created user. Primarily being used to handle the logic
           of posting reviews from the buyer
           '''

    def has_permission(self, request, view):
        if request.user.groups.filter(name='buyer').exists():
            return True
        return False
