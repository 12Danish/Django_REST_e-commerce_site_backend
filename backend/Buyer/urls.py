from django.urls import path
from .views import BuyerProductListView, BuyerProductRetrieveView

app_name = "Buyer"

urlpatterns = [
    path('', BuyerProductListView.as_view(), name="product-list"),
    path('<int:pk>/product', BuyerProductRetrieveView.as_view(), name="product-retrieve")

]
