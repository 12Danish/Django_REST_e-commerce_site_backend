from django.contrib.auth.models import User

from .test_setup_Buyer import TestSetupBuyerSerializers
from Buyer.serializers import BuyerCartListSerializer, BuyerOrderHistorySerializer, BuyerProductAddSerializer
from Buyer.models import Cart, OrderHistory


class TestBuyerSerializers(TestSetupBuyerSerializers):
    def setUp(self) -> None:
        super().setUp()
        self.cart_obj = Cart.objects.create(product_id=self.product_ids[0], quantity=1)

    def test_passed_serializing_quantity_for_adding_product(self):
        data = {"quantity": "20"}
        serializer = BuyerProductAddSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_passed_serializing_data_for_listing_product(self):
        serializer = BuyerCartListSerializer(instance=self.cart_obj)
        self.assertNotEqual(serializer, [])
        self.assertTrue(serializer.data)

    def test_passed_serializing_data_for_order_history(self):
        buyer = User.objects.create_user(username='random_user', email='random@example.com', password='password')
        hist_obj = OrderHistory.objects.create(
            buyer=buyer,
            quantity=self.cart_obj.quantity,
            product_name=self.cart_obj.product.title,
            product_image=self.cart_obj.product.image,
            product_discount=self.cart_obj.product.discount,
            product_seller=self.cart_obj.product.owner.username
        )
        serializer = BuyerOrderHistorySerializer(instance=hist_obj)
        self.assertNotEqual(serializer, [])
        self.assertTrue(serializer.data)
