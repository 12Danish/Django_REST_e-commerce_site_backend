from django.urls import path, include
from .views import SellerProductListView, SellerProductRUDView, SellerProductCreateView

app_name = 'Seller'

urlpatterns = [
    path("", include('UserManagement.urls')),
    path("homepage", SellerProductListView.as_view(), name="product-list"),
    path("homepage/create", SellerProductCreateView.as_view(), name="product-create"),
    path("<int:pk>/product", SellerProductRUDView.as_view(), name="product-retrieve"),

]
