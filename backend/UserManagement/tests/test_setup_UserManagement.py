from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetupUserManagement(APITestCase):
    def setUp(self) -> None:
        self.register_url = reverse('User_Management:register')
        self.login_url = reverse('User_Management:login')

        # Creating the groups
        Group.objects.create(name='buyer')
        Group.objects.create(name='seller')

        self.buyer_user_data = {
            "username": "testbuyer",
            "password": "danish2004",
            "email": "danishabbas2004@gmail.com",
            "is_buyer": "True",
            "is_seller": "False"
        }

        self.seller_user_data = {
            "username": "testseller",
            "password": "danish2004",
            "email": "danishabbas2004@gmail.com",
            "is_buyer": "False",
            "is_seller": "True"
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
