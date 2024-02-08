import random

from rest_framework.test import APITestCase
from faker import Faker
from ..user_serializers import PublicUserSerializer

fake = Faker()


class TestSimpleUserDisplaySerializer(APITestCase):
    def setUp(self) -> None:
        self.random_user = {
            "id": random.randint(0, 500),
            "username": fake.user_name()
        }
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_user_display_serializer(self):
        serializer = PublicUserSerializer(data=self.random_user)
        self.assertTrue(serializer.is_valid())
