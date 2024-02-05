from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from products.receivers import delete_cache_total_price, delete_cache_total_amount
from products.tasks import set_price


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


post_delete.connect(delete_cache_total_amount, sender=Category)
post_save.connect(delete_cache_total_amount, sender=Category)


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
    discount = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])

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

        if creating or (price != self.__price or discount != self.__discount):

            set_price.delay(self.pk)
            cache.delete(settings.PRICE_CACHE_NAME)

        return result

    def _do_update(self, *args, **kwargs):

        creating = not bool(self.pk)
        price = self.price
        discount = self.discount

        result = super()._do_update(*args, **kwargs)

        if creating or (price != self.__price or discount != self.__discount):
            set_price.delay(self.pk)
            cache.delete(settings.PRICE_CACHE_NAME)

        return result


post_delete.connect(delete_cache_total_price, sender=Product)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
