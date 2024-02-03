from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Seller(models.Model):
    company_name = models.CharField(max_length=255, blank=True, default=None)
    address = models.TextField()


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.ForeignKey(Seller, on_delete=models.CASCADE, default=None)
    discount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
