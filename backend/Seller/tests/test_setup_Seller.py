from django.urls import reverse
from UserManagement.tests.test_setup_UserManagement import TestSetupAuthenticationHeadersForSellerAndBuyer
from faker import Faker

fake = Faker()


class TestSetupSellerViews(TestSetupAuthenticationHeadersForSellerAndBuyer):
    '''
    This setup for the seller views creates and logs in to both seller and buyer accounts.
    Obtains access tokens for the tests to run with proper authentication
    '''

    def setUp(self) -> None:
        super().setUp()
        # Defining the urls for the seller views
        self.seller_homepage_url = reverse("Seller:product-list")
        self.seller_create_product_url = reverse("Seller:product-create")

    @staticmethod
    def get_seller_RUD_url(product_id):
        return reverse("Seller:product-retrieve", kwargs={'pk': product_id})



