from django.contrib.auth.models import User
from django.db import models


class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=14)
    city = models.CharField(max_length=100)
    neighbourhood = models.CharField(max_length=150)
    street = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField()
