import logging
from .test_setup_UserManagement import TestSetupUserManagementViews, TestSetupSimpleUserRegisterAndLogin
import pdb

# Configuring the django logging to log even the basic things
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestRegisterUserManagementView(TestSetupUserManagementViews):

    def test_failed_registration_without_credentials(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_failed_registering_with_same_username(self):
        logger.info("Entering the view")
        res1 = self.client.post(self.register_url, self.seller_user_data_1,
                                format="json")

        self.assertEqual(res1.status_code, 201)
        logger.info("The first req was made")

        res2 = self.client.post(self.register_url, self.seller_user_data_1, format="json")
        self.assertEqual(res2.status_code, 400)

    def test_failed_registering_as_buyer_and_seller_with_single_account(self):
        res = self.client.post(self.register_url, self.invalid_seller_and_buyer, format='json')
        self.assertEqual(res.status_code, 400)

    def test_successful_registration_for_buyer(self):
        res = self.client.post(self.register_url, self.buyer_user_data_1,
                               format="json")
        self.assertEqual(res.status_code, 201)

    def test_successful_registration_for_seller(self):
        res = self.client.post(self.register_url, self.seller_user_data_1,
                               format="json")
        self.assertEqual(res.status_code, 201)


class TestLoginUserManagementView(TestSetupSimpleUserRegisterAndLogin):

    def test_failed_login_no_credentials(self):
        res = self.client.post(self.login_url)
        self.assertEqual(res.status_code, 401)

    def test_failed_with_unregistered_seller(self):
        encoded_credentials = self.encode_user_credentials(self.unregistered_seller_user_data['username'],
                                                           self.unregistered_seller_user_data['password'])

        # sending the request
        res = self.send_login_request(encoded_credentials, self.unregistered_seller_user_data['is_buyer'],
                                      self.unregistered_seller_user_data['is_seller'])
        self.assertEqual(res.status_code, 403)

    def test_failed_with_invalid_password(self):
        encoded_credentials = self.encode_user_credentials(self.seller_user_data_1['username'], 'invalid_password')
        res = self.send_login_request(encoded_credentials, self.seller_user_data_1['is_buyer'],
                                      self.seller_user_data_1['is_seller'])
        self.assertEqual(res.status_code, 403)

    def test_failed_with_registered_seller_logging_as_buyer_not_registered(self):
        encoded_credentials = self.encode_user_credentials(self.seller_user_data_1['username'],
                                                           self.seller_user_data_1['password'])
        res = self.send_login_request(encoded_credentials, True, False)
        self.assertEqual(res.status_code, 404)

    def test_failed_with_registered_buyer_logging_as_seller_not_registered(self):
        encoded_credentials = self.encode_user_credentials(self.buyer_user_data_1['username'],
                                                           self.buyer_user_data_1['password'])
        res = self.send_login_request(encoded_credentials, False, True)
        self.assertEqual(res.status_code, 404)

    def test_successful_as_registered_buyer(self):
        encoded_credentials = self.encode_user_credentials(self.buyer_user_data_1['username'],
                                                           self.buyer_user_data_1['password'])
        res = self.send_login_request(encoded_credentials, self.buyer_user_data_1['is_buyer'],
                                      self.buyer_user_data_1['is_seller'])

        # Check if the response data is an instance of Token
        self.assertIsInstance(res.data.get('access'), str)
        self.assertIsInstance(res.data.get('refresh'), str)

    def test_successful_as_registered_seller(self):
        encoded_credentials = self.encode_user_credentials(self.seller_user_data_1['username'],
                                                           self.seller_user_data_1['password'])
        res = self.send_login_request(encoded_credentials, self.seller_user_data_1['is_buyer'],
                                      self.seller_user_data_1['is_seller'])

        # Check if the response data is an instance of Token
        self.assertIsInstance(res.data.get('access'), str)
        self.assertIsInstance(res.data.get('refresh'), str)
