from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_delete, sender=None)
def delete_cache_total_price(*args, **kwargs):
    cache.delete(settings.PRICE_CACHE_NAME)


@receiver(post_delete, sender=None)
def delete_cache_total_amount(*args, **kwargs):
    cache.delete(settings.CATEGORY_CACHE_NAME)
