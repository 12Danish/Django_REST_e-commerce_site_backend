'''
Seller Sign Up
Seller login
Seller Login
Buyer Sign Up
Buyer Login
'''

from django.urls import path, include
from .views import UserRegistrationView, UserLoginView

app_name = "User_Management"

urlpatterns = [
    path("register", UserRegistrationView.as_view(), name="register"),
    path("login", UserLoginView.as_view(), name="login")
]
