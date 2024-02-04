from .test_setup_UserManagement import TestSetupUserManagementSerializers
from ..serializers import UserRegisterSerializer, UserLoginSerializer
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestRegisterAndLoginSerializers(TestSetupUserManagementSerializers):
    def test_failed_registration_data_for_bot_seller_and_buyer_type(self):
        serializer = UserRegisterSerializer(data=self.invalid_user_register_data)
        self.assertFalse(serializer.is_valid())

    def test_failed_registering_data_without_type(self):
        serializer = UserRegisterSerializer(data=self.user_register_data_without_type)
        self.assertFalse(serializer.is_valid())

    def test_failed_registering_data_without_email(self):
        serializer = UserRegisterSerializer(data=self.user_register_data_without_email)
        self.assertFalse(serializer.is_valid())

    def test_passed_registering_data_with_valid_credentials(self):
        serializer = UserRegisterSerializer(data=self.valid_user_register_data)
        self.assertTrue(serializer.is_valid())

    def test_passed_logging_in_data_with_valid_credentials(self):
        serializer = UserLoginSerializer(data=self.valid_user_login_data)
        self.assertTrue(serializer.is_valid())
