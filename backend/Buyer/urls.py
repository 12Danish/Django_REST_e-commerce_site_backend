from django.urls import path
from .views import BuyerProductListView, BuyerProductRetrieveView, BuyerPostReviewView

app_name = "Buyer"

urlpatterns = [
    path('', BuyerProductListView.as_view(), name="product-list"),
    path('<int:pk>/product', BuyerProductRetrieveView.as_view(), name="product-retrieve"),
    path('<int:pk>/product/review', BuyerPostReviewView.as_view(), name="review-post")

]
