import json

from .test_setup_Buyer import TestSampleProductsForBuyerViewsSetup
from django.test import Client
import logging

# Configuring the django logging to log even the basic things
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestBuyerCartViewsForUnauthenticatedBuyer(TestSampleProductsForBuyerViewsSetup):

    def setUp(self) -> None:
        super().setUp()

    def add_product_to_cart(self):
        data = {"quantity": 10}
        headers = {"Content-Type": "application/json"}
        res = self.client.post(self.get_cart_add_url(self.product_ids[0]), data=data, format="json", headers=headers)
        logger.info(f"Posting for client 1{res.status_code, res.data}")

    def test_failed_adding_non_existent_products_to_cart(self):
        res = self.client.post(self.get_cart_add_url(1000), data={"quantity": "20"})
        self.assertEqual(res.status_code, 404)

    def test_failed_updating_non_existent_product(self):
        res = self.client.put(self.get_cart_update_url(2345), data={"quantity": "70"})
        self.assertEqual(res.status_code, 404)

    def test_failed_deleting_non_existent_product(self):
        res = self.client.delete(self.get_cart_delete_url(2345))
        self.assertEqual(res.status_code, 404)

    def test_failed_checking_out_with_empty_cart(self):
        res = self.client.get(self.checkout_url)
        self.assertEqual(res.status_code, 204)

    def test_passed_adding_products_to_cart(self):
        self.add_product_to_cart()
        self.assertIn('cart_data', self.client.session)
        self.assertEqual(len(self.client.session['cart_data']), 1)
        self.assertEqual(self.client.session['cart_data'][0]['id'], 1)

    def test_passed_retrieving_empty_cart_for_no_added_product(self):
        res = self.client.get(self.cart_list_url)
        self.assertEqual(res.data, [])

    def test_passed_retrieving_products(self):
        self.add_product_to_cart()
        res = self.client.get(self.cart_list_url)
        self.assertEqual(res.status_code, 200)
        logger.info(res.data)
        self.assertEqual(len(res.data), 1)

    def test_passed_updating_existent_product(self):
        pass

    def test_passed_deleting_existent_product(self):
        pass

    def test_passed_checking_out_with_products(self):
        pass


class TestBuyerCartViewsForAuthenticatedBuyer(TestSampleProductsForBuyerViewsSetup):
    pass
