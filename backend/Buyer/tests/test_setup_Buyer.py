import random
from faker import Faker
from django.urls import reverse

from Seller.tests.test_setup_Seller import TestSetupSellerViews
from Seller.tests.test_views_Seller import TestSellerCreateProductView

fake = Faker()


class TestCreateProductMixin:
    def create_sample_products(self):
        self.product_ids = []
        for x in range(10):
            res = self.client.post(self.seller_create_product_url,
                                   headers=random.choice([self.seller_headers_1, self.seller_headers_2]),
                                   data=TestSellerCreateProductView.complete_product_information_for_registration(),
                                   format='multipart')
            self.product_ids.append(res.data['id'])


class TestSampleProductsForBuyerViewsSetup(TestSetupSellerViews, TestCreateProductMixin):
    content_header = {"Content-Type": "application/json"}

    def setUp(self) -> None:
        super().setUp()
        self.product_list_url = reverse("Buyer:product-list")
        self.cart_list_url = reverse("Buyer:cart-list")
        self.checkout_url = reverse("Buyer:checkout")
        self.order_history_url = reverse("Buyer:order_history")
        self.create_sample_products()
        self.checkout_data = {
            "phone_num": fake.phone_number(),
            "address": fake.address(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "city": fake.city(),
            "street": fake.street_name(),
            "email": fake.email(),
            "neighbourhood": fake.word(),
        }


    @staticmethod
    def get_product_details_url(product_num):
        return reverse("Buyer:product-retrieve", kwargs={'pk': product_num})

    @staticmethod
    def get_review_post_url(product_num):
        return reverse("Buyer:review-post", kwargs={'pk': product_num})

    @staticmethod
    def get_cart_add_url(product_num):
        return reverse("Buyer:cart-add", kwargs={'pk': product_num})

    @staticmethod
    def get_cart_delete_url(product_num):
        return reverse("Buyer:cart-delete", kwargs={'pk': product_num})

    @staticmethod
    def get_cart_update_url(product_num):
        return reverse("Buyer:cart-update", kwargs={'pk': product_num})

    @staticmethod
    def get_review_data():
        return {
            "stars": random.randint(1, 5),
            "name": fake.user_name(),
            "body": fake.paragraph(nb_sentences=10)
        }

    def add_product_to_cart(self, product_id, quantity, headers_for_buyer):
        data = {"quantity": quantity}
        res = self.client.post(self.get_cart_add_url(self.product_ids[product_id]), data=data, format="json",
                               headers=headers_for_buyer)
        return res


class TestSetupBuyerSerializers(TestSetupSellerViews, TestCreateProductMixin):
    def setUp(self) -> None:
        super().setUp()
        self.create_sample_products()
