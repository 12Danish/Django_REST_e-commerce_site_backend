import base64
import logging
from .test_setup_UserManagement import TestSetupUserManagement
import pdb

# Configuring the django logging to log even the basic things
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestRegisterUserManagementView(TestSetupUserManagement):

    def setUp(self) -> None:
        super().setUp()
        self.invalid_seller_and_buyer = {
            "username": "testinvalid",
            "password": "danish2004",
            "email": "danishabbas2004@gmail.com",
            "is_buyer": "True",
            "is_seller": "True"
        }

    def test_failed_registration_without_credentials(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_failed_registering_with_same_username(self):
        logger.info("Entering the view")
        res1 = self.client.post(self.register_url, self.seller_user_data,
                                format="json")

        self.assertEqual(res1.status_code, 201)
        logger.info("The first req was made")

        res2 = self.client.post(self.register_url, self.seller_user_data, format="json")
        self.assertEqual(res2.status_code, 400)

    def test_failed_registering_as_buyer_and_seller_with_single_account(self):
        res = self.client.post(self.register_url, self.invalid_seller_and_buyer, format='json')
        self.assertEqual(res.status_code, 400)

    def test_successful_registration_for_buyer(self):
        res = self.client.post(self.register_url, self.buyer_user_data,
                               format="json")
        self.assertEqual(res.status_code, 201)

    def test_successful_registration_for_seller(self):
        res = self.client.post(self.register_url, self.seller_user_data,
                               format="json")
        self.assertEqual(res.status_code, 201)


class TestLoginUserManagementView(TestSetupUserManagement):

    def setUp(self) -> None:
        super().setUp()
        # Registering a buyer
        self.client.post(self.register_url, self.buyer_user_data,
                         format="json")
        # Registering a seller
        self.client.post(self.register_url, self.seller_user_data,
                         format="json")

        self.unregistered_buyer_user_data = {
            "username": "unregistered_buyer",
            "password": "danish2004",
            "email": "danishabbas2004@gmail.com",
            "is_buyer": "True",
            "is_seller": "False"
        }

        self.unregistered_seller_user_data = {
            "username": "unregistered_seller",
            "password": "danish2004",
            "email": "danishabbas2004@gmail.com",
            "is_buyer": "False",
            "is_seller": "True"
        }

    @staticmethod
    def encode_user_credentials(username, password):
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        return encoded_credentials

    def send_request(self, credentials, is_buyer, is_seller):
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

    def test_failed_login_no_credentials(self):
        res = self.client.post(self.login_url)
        self.assertEqual(res.status_code, 401)

    def test_failed_with_unregistered_seller(self):
        encoded_credentials = self.encode_user_credentials(self.unregistered_seller_user_data['username'],
                                                           self.unregistered_seller_user_data['password'])

        # sending the request
        res = self.send_request(encoded_credentials, self.unregistered_seller_user_data['is_buyer'],
                                self.unregistered_seller_user_data['is_seller'])
        self.assertEqual(res.status_code, 403)

    def test_failed_with_invalid_password(self):
        encoded_credentials = self.encode_user_credentials(self.seller_user_data['username'], 'invalid_password')
        res = self.send_request(encoded_credentials, self.seller_user_data['is_buyer'],
                                self.seller_user_data['is_seller'])
        self.assertEqual(res.status_code, 403)

    def test_failed_with_registered_seller_logging_as_buyer_not_registered(self):
        encoded_credentials = self.encode_user_credentials(self.seller_user_data['username'],
                                                           self.seller_user_data['password'])
        res = self.send_request(encoded_credentials, True, False)
        self.assertEqual(res.status_code, 404)

    def test_failed_with_registered_buyer_logging_as_seller_not_registered(self):
        encoded_credentials = self.encode_user_credentials(self.buyer_user_data['username'],
                                                           self.buyer_user_data['password'])
        res = self.send_request(encoded_credentials, False, True)
        self.assertEqual(res.status_code, 404)

    def test_successful_as_registered_buyer(self):
        encoded_credentials = self.encode_user_credentials(self.buyer_user_data['username'],
                                                           self.buyer_user_data['password'])
        res = self.send_request(encoded_credentials, self.buyer_user_data['is_buyer'],
                                self.buyer_user_data['is_seller'])

        # Check if the response data is an instance of Token
        self.assertIsInstance(res.data.get('access'), str)
        self.assertIsInstance(res.data.get('refresh'), str)

    def test_successful_as_registered_seller(self):
        encoded_credentials = self.encode_user_credentials(self.seller_user_data['username'],
                                                           self.seller_user_data['password'])
        res = self.send_request(encoded_credentials, self.seller_user_data['is_buyer'],
                                self.seller_user_data['is_seller'])

        # Check if the response data is an instance of Token
        self.assertIsInstance(res.data.get('access'), str)
        self.assertIsInstance(res.data.get('refresh'), str)
