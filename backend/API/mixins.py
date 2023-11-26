from rest_framework import authentication


# Defining  authentication mixin to be used in all seller views
class AuthenticationMixin():
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
