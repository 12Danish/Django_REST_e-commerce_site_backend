import pdb

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from django.db.models.functions import Coalesce
from django.utils import timezone
from django.db.models import Q, Case, When, F, DecimalField, Value
import logging

# Configuring the django logging to log even the basic things
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def one_month_ago():
    return timezone.now() - timedelta(days=30)

class ProductListSpecifications:

    def order_by_date(self, order='asc'):

        if order == 'asc':
            return self.order_by("date_created")
        elif order == 'desc':
            return self.order_by("-date_created")
        else:
            raise ValueError("Invalid order parameter. Use 'asc' or 'desc'.")
    # This method is ordering by the price


class ProductQuerySet(models.QuerySet,ProductListSpecifications):


    def order_by_date(self, order='asc'):

        if order == 'asc':
            return self.order_by("date_created")
        elif order == 'desc':
            return self.order_by("-date_created")
        else:
            raise ValueError("Invalid order parameter. Use 'asc' or 'desc'.")
    # This method is ordering by the price
    def order_by_sale_price(self, order='asc'):
        # Annotate the queryset with the sale_price property
        annotated_qs = self.annotate_sale_price()

        # Use Coalesce to handle NULL values if necessary
        annotated_qs = annotated_qs.annotate(
            sale_price_coalesced=Coalesce('sale_price', Value(0))
        )

        # Perform ordering based on the annotated sale_price
        if order.lower() == 'asc':
            return self.order_by("price").asc()
        elif order.lower() == 'desc':
            return self.order_by("price").desc()
        else:
            raise ValueError("Invalid order parameter. Use 'asc' or 'desc'.")

    # This method is used to filter out the data according to the price

    def price_filter(self, filter_type, filter_amount):
        if filter_type.lower() == "gte":
            return self.filter(price__gte=filter_amount)

        if filter_type.lower() == "lte":
            return self.filter(price__lte=filter_amount)


    # This method is being used to add extra fields to the queryset object
    def annotate_sale_price(self):
        return self.annotate(
            sale_price=Case(
                When(discount__gt=0, then=F('price') - (F('price') * F('discount') / 100)),
                default=F('price'),
                output_field=DecimalField(),
            )
        )
    def latest(self):
        logger.info("Request received  in qs latest")
        return self.filter(date_created__gte=one_month_ago())

    def popular(self):
        return self.filter(n_bought__gt=10)

    def search(self, query, user):
        lookup = Q(title__icontains=query)
        return self.filter(lookup)

    def category(self, category):
        return self.filter(category=category)

    def sale_items(self):
        return self.filter(discount__gt=0)




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

    def sale_items(self):
        return self.get_queryset().sale_items()

    def order_by_date(self, order='asc'):
        return self.get_queryset().order_by_date(order)

    def order_by_price(self, order='asc'):
        return self.get_queryset().order_by_price(order)


# This is the model for all of my products
class Product(models.Model):
    '''
           Main Product model having all the data of the products added by different sellers
           '''
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200, default="Title")
    category = models.CharField(max_length=200, default="other")
    image = models.ImageField(upload_to="", blank=True)
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
        return f'{self.title} : {self.owner} :{self.sale_price}'


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
