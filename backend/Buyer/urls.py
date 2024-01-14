from django.urls import path
from .views import BuyerProductListView, BuyerProductRetrieveView, BuyerPostReviewView, BuyerListCartAddItemView, \
    BuyerDeleteCartItemView

app_name = "Buyer"

urlpatterns = [
    path('', BuyerProductListView.as_view(), name="product-list"),
    path('<int:pk>/product', BuyerProductRetrieveView.as_view(), name="product-retrieve"),
    path('<int:pk>/product/review', BuyerPostReviewView.as_view(), name="review-post"),
    path('cart', BuyerListCartAddItemView.as_view(), name="cart-list"),
    path('<int:pk>/product/cart-add', BuyerListCartAddItemView.as_view(), name="cart-add"),
    path('<int:pk>/product/cart-delete', BuyerDeleteCartItemView.as_view(), name="cart-delete")
]
