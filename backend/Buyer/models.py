from django.db import models
from API.models import Product
from django.contrib.auth.models import User


class Cart(models.Model):
    '''
    This model is used to store the products added by the user to the cart.
    '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderHistory(models.Model):
    '''
    This model stores the products bought by the user. Although this model has the same fields as the Cart,
    it would have been counter-intuitive to store purchase-history in cart
    '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
