from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
import logging

# Configuring the django logging to log even the basic things
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ProductQuerySet(models.QuerySet):
    def latest(self):
        logger.info("Request received  in qs latest")
        return self.filter(date_created__gte=self.one_month_ago())

    def popular(self):
        return self.filter(n_bought__gt=10)

    def search(self, query, user):
        lookup = Q(title__icontains=query)
        return self.filter(lookup)

    def category(self, category):
        return self.filter(category=category)

    @staticmethod
    def one_month_ago():
        time = timezone.now() - timedelta(days=30)
        return time


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def popular(self):
        return self.get_queryset().popular()

    def latest(self):
        return self.get_queryset().latest()

    def search(self, query, user):
        return self.get_queryset().search(query, user)

    def category(self, category):
        return self.get_queryset().category(category)


# This is the model for all of my products
class Product(models.Model):
    '''
           Main Product model having all the data of the products added by different sellers
           '''
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200, default="Title")
    category = models.CharField(max_length=200, default="other")
    image = models.ImageField(upload_to="",
                              default="C:/Users/Sheryar/PycharmProjects/construction_site/frontend/src/assets/images/sample_product.jpg")
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    n_bought = models.PositiveIntegerField(default=0)
    discount = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    date_created = models.DateTimeField(auto_created=True, default=datetime.now)
    objects = ProductManager()

    @property
    def sale_item(self):
        if self.discount:
            return True
        return False
        # The property for sale_price

    @property
    def sale_price(self):
        if self.discount:
            return "%.2f" % (float(self.price) - (float(self.price) * float(self.discount) / 100))
        else:
            return self.price

    # Representation for model Instances
    def __str__(self):
        return f'{self.title} : {self.owner}'


# This is the model which will have all the reviews of different products by different users
class Review(models.Model):
    '''
               Main Reviews  model having all the data of the reviews  added by different buyers
               '''
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100, default="random")
    stars = models.PositiveIntegerField(default=0)
    product = models.ForeignKey('Product', related_name="review", on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.reviewer} {self.product}'
