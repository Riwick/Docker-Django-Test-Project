from django.contrib.auth.models import User
from django.db import models

from products.tasks import set_price


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Seller(models.Model):
    company_name = models.CharField(max_length=255, blank=False, default=None)
    address = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=False)

    def __str__(self):
        return self.company_name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    price = models.PositiveIntegerField()
    price_with_discount = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(Seller, on_delete=models.CASCADE, default=None)
    discount = models.PositiveIntegerField(default=0)

    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, default=None)

    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__price = self.price
        self.__discount = self.discount

    def save(self, *args, **kwargs):
        creating = not bool(self.pk)
        price = self.price
        discount = self.discount

        result = super().save(*args, **kwargs)

        if creating:
            set_price.delay(self.pk)

        if price != self.__price or discount != self.__discount:

            set_price.delay(self.pk)

        return result


