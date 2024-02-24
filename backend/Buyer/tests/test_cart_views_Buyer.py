import pdb

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

    def test_failed_accessing_order_history_without_login(self):
        self.add_product_to_cart()
        self.client.get(self.checkout_url)
        res = self.client.get(self.order_history_url)
        self.assertEqual(res.status_code, 401)

    def test_passed_adding_products_to_cart(self):
        self.add_product_to_cart()
        self.assertIn('cart_data', self.client.session)
        self.assertEqual(len(self.client.session['cart_data']), 1)
        self.assertEqual(self.client.session['cart_data'][0]['id'], 1)

    def test_passed_retrieving_empty_cart_for_no_added_product(self):
        res = self.client.get(self.cart_list_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [])

    def test_passed_retrieving_products(self):
        self.add_product_to_cart()
        res = self.client.get(self.cart_list_url)
        self.assertEqual(res.status_code, 200)
        logger.info(res.data)
        self.assertEqual(len(res.data), 1)

    def test_passed_updating_existent_product(self):
        self.add_product_to_cart()
        res = self.client.put(self.get_cart_update_url(1), data={"quantity": 70}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.client.session['cart_data'][0]['quantity'], 70)

    def test_passed_deleting_existent_product(self):
        self.add_product_to_cart()
        res = self.client.delete(self.get_cart_delete_url(1))
        self.assertEqual(res.status_code, 204)

    def test_passed_checking_out_with_products(self):
        self.add_product_to_cart()
        res1 = self.client.get(self.checkout_url)
        self.assertEqual(res1.status_code, 200)
        res2 = self.client.get(self.cart_list_url)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.data, [])


class TestBuyerCartViewsForAuthenticatedBuyer(TestSampleProductsForBuyerViewsSetup):
    def add_product_to_cart(self, product_id, quantity, headers_for_buyer):
        data = {"quantity": quantity}
        res = self.client.post(self.get_cart_add_url(self.product_ids[product_id]), data=data, format="json",
                               headers=headers_for_buyer)
        logger.info(f"Posting for client {res.status_code} {res.data}")
        return res

    def test_passed_adding_products_to_cart(self):
        res = self.add_product_to_cart(product_id=0, quantity=7, headers_for_buyer=self.buyer_headers_1)
        self.assertEqual(res.status_code, 201)

    def test_passed_retrieving_relevant_items(self):
        self.add_product_to_cart(product_id=6, quantity=89, headers_for_buyer=self.buyer_headers_1)
        self.add_product_to_cart(product_id=0, quantity=7, headers_for_buyer=self.buyer_headers_2)
        res1 = self.client.get(self.cart_list_url, headers=self.buyer_headers_1)
        logger.info(f"This is the first buyer {res1.data}")
        res2 = self.client.get(self.cart_list_url, headers=self.buyer_headers_2)
        logger.info(f"This is the second buyer {res2.data}")
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(89, res1.data[0]['quantity'])
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(7, res2.data[0]['quantity'])

    def test_passed_updating_products(self):
        self.add_product_to_cart(product_id=6, quantity=89, headers_for_buyer=self.buyer_headers_1)
        res = self.client.put(self.get_cart_update_url(1), data={"quantity": 70}, format="json",
                              headers=self.buyer_headers_1)
        self.assertEqual(res.status_code, 200)

    def test_passed_deleting_product_by_user(self):
        self.add_product_to_cart(product_id=6, quantity=89, headers_for_buyer=self.buyer_headers_1)
        self.add_product_to_cart(product_id=0, quantity=7, headers_for_buyer=self.buyer_headers_2)
        res1_del = self.client.delete(self.get_cart_delete_url(1), headers=self.buyer_headers_1)
        self.assertEqual(res1_del.status_code, 204)
        res1_get = self.client.get(self.cart_list_url, headers=self.buyer_headers_1)
        self.assertEqual(len(res1_get.data), 0)
        res2_get = self.client.get(self.cart_list_url, headers=self.buyer_headers_2)
        self.assertNotEqual(len(res2_get.data), 0)

    def test_passed_checking_out_and_viewing_order_history(self):
        self.add_product_to_cart(product_id=6, quantity=89, headers_for_buyer=self.buyer_headers_1)
        res1 = self.client.get(self.checkout_url, headers=self.buyer_headers_1)
        self.assertEqual(res1.status_code, 200)
        # Checking the cart is empty
        res1_check = self.client.get(self.cart_list_url, headers=self.buyer_headers_1)
        self.assertEqual(res1_check.status_code, 200)
        self.assertEqual(res1_check.data, [])
        # Checking that order history has been made
        res2 = self.client.get(self.order_history_url, headers=self.buyer_headers_1)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(len(res2.data), 1)
