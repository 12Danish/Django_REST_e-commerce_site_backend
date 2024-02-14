from django.db import models
from API.models import Product
from django.contrib.auth.models import User

'''
Need to handle logic of what to do when seller deletes a product
'''


class Cart(models.Model):
    '''
    This model is used to store the products added by the user to the cart.
    The registered buyer will be null if the user is not authenticated
    The unregistered buyer will be null if the user is authenticated
    '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    device_id = models.CharField(null=True, blank=True, max_length=200)


class OrderHistory(models.Model):
    '''
    This model stores the products bought by the user. Although this model has the same fields as the Cart,
    it would have been counter-intuitive to store purchase-history in cart.
    The reason why a foreign key is not used is because if a product is deleted by the seller it should still
    appear to the buyer if he ever bought it.
    '''
    product_name = models.CharField(max_length=200)
    product_price = models.PositiveIntegerField(null=True)
    product_seller = models.CharField(max_length=200)
    product_discount = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    product_image = models.ImageField(upload_to="")
    quantity = models.PositiveIntegerField(null=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
