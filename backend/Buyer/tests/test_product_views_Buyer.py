from datetime import datetime
from django.utils import timezone

from .test_setup_Buyer import TestSampleProductsForBuyerViewsSetup
from API.models import one_month_ago
import logging

# Configuring the django logging to log even the basic things
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestBuyerProductViews(TestSampleProductsForBuyerViewsSetup):

    def test_successful_displaying_latest_products(self):
        res = self.client.get(self.product_list_url)
        logger.info(res.data)
        for product_data in res.data['results']:
            date_created = datetime.strptime(product_data['date_created'], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            self.assertGreaterEqual(date_created, one_month_ago())

    def test_successful_displaying_popular_products(self):
        res = self.client.get(self.product_list_url + "?popular=True")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['results'], [])

    def test_successful_displaying_category_wise_products(self):
        res = self.client.get(self.product_list_url + "?category=test_category")
        logger.info(res.data)
        for product_data in res.data['results']:
            self.assertEqual(product_data['category'], "test_category")

    def test_successful_displaying_searched_products(self):
        res = self.client.get(self.product_list_url + "?search=s")
        logger.info(res.data)
        for product_data in res.data['results']:
            self.assertIn('s', product_data['title'].lower())

    def test_successful_displaying_sale_items(self):
        res = self.client.get(self.product_list_url + "?sale=True")
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.data, [])

    def test_successful_ordering_products_by_date_in_ascending_order(self):
        # Send a GET request to the product list URL with order_by and order parameters
        res = self.client.get(self.product_list_url + "?order_by=date&order=asc")

        # Check if the response status code is 200 (OK)
        self.assertEqual(res.status_code, 200)

        # Log the data returned in the response
        logging.info(f"Response data: {res.data}")

        # Check if the products are ordered by date in ascending order
        ordered_products = res.data['results']
        dates = [product['date_created'] for product in ordered_products]

        # Convert date strings to datetime objects for comparison
        dates_as_datetime = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

        # Confirm that dates are in ascending order
        self.assertEqual(dates_as_datetime, sorted(dates_as_datetime))

    def test_successful_ordering_products_by_date_in_descending_order(self):
        # Send a GET request to the product list URL with order_by and order parameters for descending order
        res = self.client.get(self.product_list_url + "?order_by=date&order=desc")

        # Check if the response status code is 200 (OK)
        self.assertEqual(res.status_code, 200)

        # Log the data returned in the response
        logging.info(f"Response data: {res.data}")

        # Check if the products are ordered by date in descending order
        ordered_products = res.data['results']
        dates = [product['date_created'] for product in ordered_products]

        # Convert date strings to datetime objects for comparison
        dates_as_datetime = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

        # Confirm that dates are in descending order
        self.assertEqual(dates_as_datetime, sorted(dates_as_datetime, reverse=True))

    def test_successful_ordering_products_by_ascending_price(self):
        # Send a GET request to the product list URL with order_by and order parameters for ascending price
        res = self.client.get(self.product_list_url + "?order_by=price&order=asc")

        # Check if the response status code is 200 (OK)
        self.assertEqual(res.status_code, 200)

        # Check if the products are ordered by price in ascending order
        ordered_products = res.data['results']
        prices = [product['price'] for product in ordered_products]

        # Confirm that prices are in ascending order
        for index in range(len(prices) - 1):
            self.assertLessEqual(float(prices[index]), float(prices[index + 1]))

    def test_successful_ordering_products_by_descending_price(self):
        # Send a GET request to the product list URL with order_by and order parameters for descending price
        res = self.client.get(self.product_list_url + "?order_by=price&order=desc")

        # Check if the response status code is 200 (OK)
        self.assertEqual(res.status_code, 200)
        # Check if the products are ordered by price in descending order
        ordered_products = res.data['results']
        prices = [product['price'] for product in ordered_products]


        # Confirm that prices are in ascending order
        for index in range(len(prices) - 1):
            self.assertGreaterEqual(float(prices[index]), float(prices[index + 1]))


    def test_successful_filtering_products_on_price(self):
        res = self.client.get(self.product_list_url + "?filter_type=gte&filter_amount=1000")
        self.assertEqual(res.status_code, 200)

        # Check if the products are ordered by price in ascending order
        ordered_products = res.data['results']
        prices = [product['price'] for product in ordered_products]
        for price in prices:
            self.assertGreaterEqual(float(price), 1000.00)


    def test_successful_retrieving_product(self):
        res = self.client.get(self.get_product_details_url(self.product_ids[0]))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['id'], self.product_ids[0])

    def test_failed_posting_review_as_anonymous_user(self):
        res = self.client.post(self.get_review_post_url(self.product_ids[0]), data=self.get_review_data())
        self.assertEqual(res.status_code, 401)

    def test_failed_posting_review_as_seller(self):
        res = self.client.post(self.get_review_post_url(self.product_ids[0]), headers=self.seller_headers_1,
                               data=self.get_review_data())
        self.assertEqual(res.status_code, 403)

    def test_passed_posting_review_as_authenticated_buyer(self):
        res = self.client.post(self.get_review_post_url(self.product_ids[0]), headers=self.buyer_headers_1,
                               data=self.get_review_data(), format='json')
        self.assertEqual(res.status_code, 201)
