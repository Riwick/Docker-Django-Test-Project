from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_save

from products.receivers import delete_cache_total_price, delete_cache_total_amount, delete_cache_basket_total_sum, \
    delete_cache_favorites_products_total_sum
from products.tasks import set_price


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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


post_save.connect(delete_cache_total_price, sender=Product)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Профиль {self.user.username}'


class BasketProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Корзина для {self.user.username}'


post_save.connect(delete_cache_basket_total_sum, sender=BasketProducts)


class FavoritesProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'Избранные продукты {self.user.username}'


post_save.connect(delete_cache_favorites_products_total_sum, sender=FavoritesProducts)


class FavoritesCategories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'Избранные категории {self.user.username}'





