from django.urls import path
from .buyer_product_views import BuyerProductListView, BuyerProductRetrieveView, BuyerPostReviewView
from .buyer_cart_views import BuyerDeleteCartItemView, BuyerCartAddItemView, BuyerUpdateCartItemView, \
    BuyerCheckoutView, BuyerOrderHistory, BuyerListCartItemView

app_name = "Buyer"

urlpatterns = [
    path('', BuyerProductListView.as_view(), name="product-list"),
    path('<int:pk>/product', BuyerProductRetrieveView.as_view(), name="product-retrieve"),
    path('<int:pk>/product/review', BuyerPostReviewView.as_view(), name="review-post"),
    path('cart', BuyerListCartItemView.as_view(), name="cart-list"),
    path('<int:pk>/product/cart-add', BuyerCartAddItemView.as_view(), name="cart-add"),
    path('<int:pk>/cart/cart-delete', BuyerDeleteCartItemView.as_view(), name="cart-delete"),
    path('<int:pk>/cart/cart-update', BuyerUpdateCartItemView.as_view(), name='cart-update'),
    path('cart/checkout', BuyerCheckoutView.as_view(), name="checkout"),
    path('order_history', BuyerOrderHistory.as_view(), name="order_history")
]
