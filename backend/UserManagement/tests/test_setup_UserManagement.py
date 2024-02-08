from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
import base64

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

        self.buyer_user_data_1 = {
            "username": fake.user_name(),
            "password": fake.password(),
            "email": fake.email(),
            "is_buyer": "True",
            "is_seller": "False"
        }

        self.seller_user_data_1 = {
            "username": fake.user_name(),
            "password": fake.password(),
            "email": fake.email(),
            "is_buyer": "False",
            "is_seller": "True"
        }

        self.buyer_user_data_2 = {
            "username": fake.user_name(),
            "password": fake.password(),
            "email": fake.email(),
            "is_buyer": "True",
            "is_seller": "False"
        }

        self.seller_user_data_2 = {
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


class TestSetupSimpleUserRegisterAndLogin(TestSetupUserManagementViews):

    def setUp(self) -> None:
        super().setUp()
        # Registering  buyer 1
        self.client.post(self.register_url, self.buyer_user_data_1,
                         format="json")
        # Registering a seller 1
        self.client.post(self.register_url, self.seller_user_data_1,
                         format="json")
        # Registering a buyer 2
        self.client.post(self.register_url, self.buyer_user_data_2,
                         format="json")
        # Registering a seller 2
        self.client.post(self.register_url, self.seller_user_data_2,
                         format="json")

    @staticmethod
    def encode_user_credentials(username, password):
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        return encoded_credentials

    def send_login_request(self, credentials, is_buyer, is_seller):
        authentication_header = f"Basic {credentials}"

        # Request body data
        data = {
            "is_buyer": is_buyer,  # or False based on your requirements
            "is_seller": is_seller  # or True based on your requirements
            # Include other required fields in your data...
        }

        # Make the POST request with authentication header and data
        return self.client.post(
            self.login_url,
            data=data,
            format="json",
            HTTP_AUTHORIZATION=authentication_header
        )


class TestSetupAuthenticationHeadersForSellerAndBuyer(TestSetupSimpleUserRegisterAndLogin):
    '''
    This setup for the seller views creates and logs in to both seller and buyer accounts.
    Obtains access tokens for the tests to run with proper authentication
    '''

    def setUp(self) -> None:
        super().setUp()
        # Encoding the credentials for one set of buyer and seller
        encoded_credentials_seller_1 = self.encode_user_credentials(self.seller_user_data_1['username'],
                                                                    self.seller_user_data_1['password'])
        encoded_credentials_buyer_1 = self.encode_user_credentials(self.buyer_user_data_1['username'],
                                                                   self.seller_user_data_1['password'])
        # Encoding credentials for other set of buyer and seller
        encoded_credentials_seller_2 = self.encode_user_credentials(self.seller_user_data_2['username'],
                                                                    self.seller_user_data_2['password'])
        encoded_credentials_buyer_2 = self.encode_user_credentials(self.buyer_user_data_2['username'],
                                                                   self.seller_user_data_2['password'])

        # Sending the request and storing the access_tokens
        res_seller_1 = self.send_login_request(encoded_credentials_seller_1, self.seller_user_data_1['is_buyer'],
                                               self.seller_user_data_1['is_seller'])

        access_token_seller_1 = res_seller_1.data.get('access')
        res_buyer_1 = self.send_login_request(encoded_credentials_buyer_1, self.buyer_user_data_1['is_buyer'],
                                              self.buyer_user_data_1['is_seller'])
        access_token_buyer_1 = res_buyer_1.data.get('access')

        res_seller_2 = self.send_login_request(encoded_credentials_seller_2, self.seller_user_data_2['is_buyer'],
                                               self.seller_user_data_2['is_seller'])

        access_token_seller_2 = res_seller_2.data.get('access')
        res_buyer_2 = self.send_login_request(encoded_credentials_buyer_2, self.buyer_user_data_2['is_buyer'],
                                              self.buyer_user_data_2['is_seller'])
        access_token_buyer_2 = res_buyer_2.data.get('access')

        # creating the authorization headers for seller and buyer
        self.seller_headers_1 = {'Authorization': f'Bearer {access_token_seller_1}'}
        self.buyer_headers_1 = {'Authorization': f'Bearer {access_token_buyer_1}'}
        self.seller_headers_2 = {'Authorization': f'Bearer {access_token_seller_2}'}
        self.buyer_headers_2 = {'Authorization': f'Bearer {access_token_buyer_2}'}
