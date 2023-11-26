'''
Seller Sign Up
Seller login
Seller Login
Buyer Sign Up
Buyer Login
'''

from django.urls import path, include
from . import views

app_name = "User_Management"

urlpatterns = [
    path("", views.PlaceHolderView.as_view())
]
