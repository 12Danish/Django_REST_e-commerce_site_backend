from django.db import IntegrityError
from rest_framework.utils import json
import logging
from .test_setup_UserManagement import TestSetupUserManagement
import pdb

# Configuring the django logging to log even the basic things
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestRegisterUserManagementView(TestSetupUserManagement):
    def test_failed_registration_without_credentials(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_successful_registration_for_buyer(self):
        res = self.client.post(self.register_url, self.buyer_user_data,
                               format="json")
        self.assertEqual(res.status_code, 201)

    def test_error_registering_with_same_username(self):
        logger.info("Entering the view")
        res1 = self.client.post(self.register_url, self.seller_user_data,
                                format="json")

        self.assertEqual(res1.status_code, 201)
        logger.info("The first req was made")

        res2 = self.client.post(self.register_url, self.seller_user_data, format="json")
        self.assertEqual(res2.status_code, 400)

    def test_successful_registration_for_seller(self):
        res = self.client.post(self.register_url, self.seller_user_data,
                               format="json")
        self.assertEqual(res.status_code, 201)
