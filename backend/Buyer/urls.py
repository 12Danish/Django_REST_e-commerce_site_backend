from django.urls import path
from .views import BuyerProductListView

app_name = "Buyer"

urlpatterns = [
    path('', BuyerProductListView.as_view(), name="homepage")
    
]
