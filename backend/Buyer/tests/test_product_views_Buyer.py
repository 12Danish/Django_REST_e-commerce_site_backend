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
        for product_data in res.data:
            date_created = datetime.strptime(product_data['date_created'], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            self.assertGreaterEqual(date_created, one_month_ago())

    def test_successful_displaying_popular_products(self):
        res = self.client.get(self.product_list_url + "?popular=True")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [])

    def test_successful_displaying_category_wise_products(self):
        res = self.client.get(self.product_list_url + "?category=test_category")
        logger.info(res.data)
        for product_data in res.data:
            self.assertEqual(product_data['category'], "test_category")

    def test_successful_displaying_searched_products(self):
        res = self.client.get(self.product_list_url + "?search=s")
        logger.info(res.data)
        for product_data in res.data:
            self.assertIn('s', product_data['title'].lower())

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
