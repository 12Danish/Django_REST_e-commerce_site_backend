import random
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from .test_setup_Seller import TestSetupSellerViews
from faker import Faker
import logging

# Configuring the django logging to log even the basic things
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

fake = Faker()


class TestSellerAccess(TestSetupSellerViews):

    def test_failed_with_unregistered_user(self):
        res = self.client.get(self.seller_homepage_url)
        self.assertEqual(res.status_code, 401)

    def test_failed_with_registered_buyer(self):
        res = self.client.get(self.seller_homepage_url, headers=self.buyer_headers_1)
        self.assertEqual(res.status_code, 403)

    def test_passed_with_registered_seller(self):
        res = self.client.get(self.seller_homepage_url, headers=self.seller_headers_1)
        self.assertEqual(res.status_code, 200)


class TestSellerCreateProductView(TestSetupSellerViews):
    @staticmethod
    def temporary_image():
        bts = BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(bts, 'jpeg')
        return SimpleUploadedFile("new_image_test.jpg", bts.getvalue())

    @staticmethod
    def complete_product_information_for_registration():
        return {
            'title': fake.name(),
            'price': random.randint(2, 10000),
            'image': TestSellerCreateProductView.temporary_image(),
            'description': fake.name(),
            'discount': 5,
            'category': 'test_category'
        }

    def test_failed_with_incomplete_data(self):
        data = {
            'title': fake.name(),
            'image': self.temporary_image(),
            'description': fake.name(),
            'discount': 5
        }
        res = self.client.post(self.seller_create_product_url, headers=self.seller_headers_1, data=data,
                               format='multipart')
        self.assertEqual(res.status_code, 400)

    def test_failed_with_negative_price(self):
        data = {
            'title': fake.name(),
            'price': -7,
            'image': self.temporary_image(),
            'description': fake.name(),
            'discount': 5
        }
        res = self.client.post(self.seller_create_product_url, headers=self.seller_headers_1, data=data,
                               format='multipart')
        self.assertEqual(res.status_code, 400)

    def test_failed_with_negative_discount(self):
        data = {
            'title': fake.name(),
            'price': 7,
            'image': self.temporary_image(),
            'description': fake.name(),
            'discount': -5
        }
        res = self.client.post(self.seller_create_product_url, headers=self.seller_headers_1, data=data,
                               format='multipart')
        self.assertEqual(res.status_code, 400)

    def test_failed_registering_with_same_name_twice_with_same_user(self):
        data = self.complete_product_information_for_registration()
        res1 = self.client.post(self.seller_create_product_url, headers=self.seller_headers_1, data=data,
                                format='multipart')
        self.assertEqual(res1.status_code, 201)
        res2 = self.client.post(self.seller_create_product_url, headers=self.seller_headers_1, data=data,
                                format='multipart')
        self.assertEqual(res2.status_code, 400)

    def test_passed_registering_with_same_name_twice_but_diff_user(self):
        data = self.complete_product_information_for_registration()
        res1 = self.client.post(self.seller_create_product_url, headers=self.seller_headers_1, data=data,
                                format='multipart')
        self.assertEqual(res1.status_code, 201)
        res2 = self.client.post(self.seller_create_product_url, headers=self.seller_headers_2, data=data,
                                format='multipart')
        self.assertEqual(res1.status_code, 201)

    def test_passed_with_complete_information(self):
        data = self.complete_product_information_for_registration()
        res = self.client.post(self.seller_create_product_url, headers=self.seller_headers_1, data=data,
                               format='multipart')
        self.assertEqual(res.status_code, 201)

    def test_passed_with_proper_data_without_discount(self):
        data = {
            'title': fake.name(),
            'price': random.randint(2, 10000),
            'image': self.temporary_image(),
            'description': fake.name(),
        }
        res = self.client.post(self.seller_create_product_url, headers=self.seller_headers_1, data=data,
                               format='multipart')
        self.assertEqual(res.status_code, 201)

    def test_passed_with_proper_data_without_image(self):
        data = {
            'title': fake.name(),
            'price': random.randint(2, 10000),
            'description': fake.name(),
            'discount': 5
        }
        res = self.client.post(self.seller_create_product_url, headers=self.seller_headers_1, data=data,
                               format='multipart')
        self.assertEqual(res.status_code, 201)


class TestSellerListView(TestSetupSellerViews):

    def setUp(self) -> None:
        super().setUp()
        self.product_data1 = {
            'title': fake.name(),
            'price': random.randint(2, 10000),
            'description': fake.name(),
            'discount': 5
        }

        self.product_data2 = {
            'title': fake.name(),
            'price': random.randint(2, 10000),
            'description': fake.name(),
            'discount': 5
        }

    def test_empty_set_returned_with_no_published_products(self):
        res = self.client.get(self.seller_homepage_url, headers=self.seller_headers_1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [])

    def test_empty_set_returned_for_no_published_products_even_with_other_sellers_with_products(self):
        self.client.post(self.seller_create_product_url, headers=self.seller_headers_1, data=self.product_data1,
                         format='multipart')

        res = self.client.get(self.seller_homepage_url, headers=self.seller_headers_2)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [])

    def test_relevant_data_returned_only(self):
        self.client.post(self.seller_create_product_url, headers=self.seller_headers_1, data=self.product_data1,
                         format='multipart')

        self.client.post(self.seller_create_product_url, headers=self.seller_headers_2, data=self.product_data2,
                         format='multipart')

        res1 = self.client.get(self.seller_homepage_url, headers=self.seller_headers_1)
        self.assertEqual(res1.status_code, 200)
        self.assertIsNotNone(self.product_data1['title'])
        self.assertEqual(self.product_data1['title'], res1.data[0]['title'])
        res2 = self.client.get(self.seller_homepage_url, headers=self.seller_headers_2)
        self.assertEqual(res2.status_code, 200)

        self.assertEqual(self.product_data2['title'], res2.data[0]['title'])

    def test_specified_data_returned_only(self):
        self.client.post(self.seller_create_product_url, headers=self.seller_headers_1, data=self.product_data1,
                         format='multipart')
        self.client.post(self.seller_create_product_url, headers=self.seller_headers_1, data=self.product_data2,
                         format='multipart')

        res = self.client.get(self.seller_homepage_url + "?search=a", headers=self.seller_headers_1)
        logger.info(res.data)
        for product_data in res.data:
            self.assertIn('a', product_data['title'].lower())


class TestSellerRUDViews(TestSetupSellerViews):
    def setUp(self) -> None:
        super().setUp()
        data = {
            'title': fake.name(),
            'price': random.randint(2, 10000),
            'description': fake.name(),
            'discount': 5
        }
        post_req = self.client.post(self.seller_create_product_url, headers=self.seller_headers_1, data=data,
                                    format='multipart')
        self.product_id = post_req.data['id']

    def test_failed_in_retrieving_non_existent_product(self):
        res = self.client.get(self.get_seller_RUD_url(10), headers=self.seller_headers_1)
        self.assertEqual(res.status_code, 404)

    def test_failed_in_updating_non_existent_product(self):
        res = self.client.put(self.get_seller_RUD_url(10), headers=self.seller_headers_1, data={"price": 500})
        self.assertEqual(res.status_code, 404)

    def test_failed_in_deleting_non_existent_product(self):
        res = self.client.delete(self.get_seller_RUD_url(10), headers=self.seller_headers_1)
        self.assertEqual(res.status_code, 404)

    def test_successful_in_retrieving_existent_data(self):
        res = self.client.get(self.get_seller_RUD_url(self.product_id), headers=self.seller_headers_1)
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.data, [])
        self.assertEqual(res.data['id'], self.product_id)

    def test_successful_in_updating_existent_data(self):
        res = self.client.put(self.get_seller_RUD_url(self.product_id), headers=self.seller_headers_1,
                              data={"price": 500})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['id'], self.product_id)
        self.assertEqual(res.data['price'], '500.00')

    def test_successful_in_deleting_existent_data(self):
        res = self.client.delete(self.get_seller_RUD_url(self.product_id), headers=self.seller_headers_1)
        self.assertEqual(res.status_code, 204)
