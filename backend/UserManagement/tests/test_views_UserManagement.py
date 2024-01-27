from rest_framework.utils import json

from .test_setup_UserManagement import TestSetupUserManagement
import pdb


class TestRegisterUserManagementView(TestSetupUserManagement):
    def test_failed_registration_without_credentials(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_successful_registration_for_buyer(self):
        res = self.client.post(self.register_url, self.buyer_user_data,
                               format="json")
        self.assertEqual(res.status_code, 201)

    def test_succesfull_registration_for_seller(self):
        res = self.client.post(self.register_url, self.seller_user_data,
                               format="json")
        self.assertEqual(res.status_code, 201)
