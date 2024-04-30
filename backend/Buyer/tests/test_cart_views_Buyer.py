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
        res = self.client.post(self.get_cart_add_url(self.product_ids[0]), data=data, format="json",
                               headers=self.content_header)
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
        res = self.client.post(self.checkout_url, data=self.checkout_data, headers=self.content_header, format='json')
        self.assertEqual(res.status_code, 404)

    def test_failed_accessing_order_history_without_login(self):
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
        self.assertEqual(res.data['results'], [])

    def test_passed_retrieving_products(self):
        self.add_product_to_cart()
        res = self.client.get(self.cart_list_url)
        self.assertEqual(res.status_code, 200)
        logger.info(res.data)
        self.assertEqual(len(res.data['results']), 1)

    def test_passed_updating_existent_product(self):
        self.add_product_to_cart()
        res = self.client.put(self.get_cart_update_url(1), data={"quantity": 70}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.client.session['cart_data'][0]['quantity'], 70)

    def test_passed_deleting_existent_product(self):
        self.add_product_to_cart()
        res = self.client.delete(self.get_cart_delete_url(1))
        self.assertEqual(res.status_code, 204)

    def test_passed_empty_set_returned_for_unregistered_user_sending_get_req_to_checkout(self):
        res = self.client.get(self.checkout_url)
        self.assertEqual(res.status_code, 404)

        self.assertEqual(res.data, [])

    def test_passed_checking_out_with_products(self):
        self.add_product_to_cart()
        res1 = self.client.post(self.checkout_url, headers=self.content_header, data=self.checkout_data, format="json")
        logger.info(res1.data)
        self.assertEqual(res1.status_code, 200)
        res2 = self.client.get(self.cart_list_url)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.data['results'], [])


class TestBuyerCartViewsForAuthenticatedBuyer(TestSampleProductsForBuyerViewsSetup):

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
        self.assertEqual(res1.data['results'][0]['quantity'], 89)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.data['results'][0]['quantity'], 7)

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
        self.assertEqual(len(res1_get.data['results']), 0)
        res2_get = self.client.get(self.cart_list_url, headers=self.buyer_headers_2)
        self.assertNotEqual(len(res2_get.data['results']), 0)


class TestCheckoutFunctionalityForAuthenticatedBuyer(TestSampleProductsForBuyerViewsSetup):
    def setUp(self) -> None:
        super().setUp()
        self.add_product_to_cart(product_id=6, quantity=89, headers_for_buyer=self.buyer_headers_1)
        self.res1_post = self.client.post(self.checkout_url, headers=self.buyer_headers_1, data=self.checkout_data,
                                          format="json")
        self.res1_check = self.client.get(self.cart_list_url, headers=self.buyer_headers_1)

    def test_passed_checking_out_and_viewing_order_history(self):
        self.assertEqual(self.res1_post.status_code, 200)
        # Checking the cart is empty

        self.assertEqual(self.res1_check.status_code, 200)
        self.assertEqual(self.res1_check.data['results'], [])
        # Checking that order history has been made
        order_his_res = self.client.get(self.order_history_url, headers=self.buyer_headers_1)
        self.assertEqual(order_his_res.status_code, 200)
        self.assertEqual(len(order_his_res.data['results']), 1)

    def test_passed_retrieving_user_info_using_get(self):
        res_get = self.client.get(self.checkout_url, headers=self.buyer_headers_1)
        self.assertEqual(res_get.status_code, 200)
        self.assertNotEqual(res_get.data, [])

    def test_passed_updating_data_from_checkout(self):
        self.checkout_data["first_name"] = "Azha"
        self.checkout_data["city"] = "Mumbai"

        self.add_product_to_cart(product_id=1, quantity=79, headers_for_buyer=self.buyer_headers_1)

        self.client.post(self.checkout_url, headers=self.buyer_headers_1, data=self.checkout_data,
                         format="json")
        res_get = self.client.get(self.checkout_url, headers=self.buyer_headers_1)
        self.assertEqual(res_get.status_code, 200)
        self.assertEqual(res_get.data['first_name'], "Azha")
        self.assertEqual(res_get.data['city'], "Mumbai")
