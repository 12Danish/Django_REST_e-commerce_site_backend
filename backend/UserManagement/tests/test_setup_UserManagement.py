from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker

fake = Faker()


class TestSetupUserManagementViews(APITestCase):
    '''
    Creating the setup for testing the registering and login functionality
    '''

    def setUp(self) -> None:
        self.register_url = reverse('User_Management:register')
        self.login_url = reverse('User_Management:login')

        # Creating the groups
        Group.objects.create(name='buyer')
        Group.objects.create(name='seller')

        self.buyer_user_data = {
            "username": fake.user_name(),
            "password": fake.password(),
            "email": fake.email(),
            "is_buyer": "True",
            "is_seller": "False"
        }

        self.seller_user_data = {
            "username": fake.user_name(),
            "password": fake.password(),
            "email": fake.email(),
            "is_buyer": "False",
            "is_seller": "True"
        }

        self.invalid_seller_and_buyer = {
            "username": fake.user_name(),
            "password": fake.password(),
            "email": fake.email(),
            "is_buyer": "True",
            "is_seller": "True"
        }
        self.unregistered_buyer_user_data = {
            "username": fake.user_name(),
            "password": fake.password(),
            "email": fake.email(),
            "is_buyer": "True",
            "is_seller": "False"
        }

        self.unregistered_seller_user_data = {
            "username": fake.user_name(),
            "password": fake.password(),
            "email": fake.email(),
            "is_buyer": "False",
            "is_seller": "True"
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()


class TestSetupUserManagementSerializers(APITestCase):
    def setUp(self) -> None:
        self.valid_user_register_data = {
            "username": fake.user_name(),
            "password": fake.password(),
            "email": fake.email(),
            "is_buyer": "False",
            "is_seller": "True"
        }
        self.invalid_user_register_data = {
            "username": fake.user_name(),
            "password": fake.password(),
            "email": fake.email(),
            "is_buyer": "True",
            "is_seller": "True"
        }

        self.user_register_data_without_type = {
            "username": fake.user_name(),
            "password": fake.password(),
            "email": fake.email(),
        }
        self.user_register_data_without_email = {
            "username": fake.user_name(),
            "password": fake.password(),
            "is_buyer": "False",
            "is_seller": "True"
        }

        self.valid_user_login_data = {

                "username": fake.user_name(),
                "password": fake.password(),
                "is_buyer": "False",
                "is_seller": "True"
            }

