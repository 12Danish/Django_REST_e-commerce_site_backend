from django.urls import path, include

urlpatterns = [
    path("", include("Buyer.urls")),
    path("seller/", include("Seller.urls"))
]
