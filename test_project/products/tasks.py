from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction
from django.db.models import F


@shared_task(base=Singleton)
def set_price(product_id):
    from products.models import Product

    with transaction.atomic():

        product = (Product.objects.select_for_update().filter(id=product_id).
                   annotate(annotated_price=F('price') - (F('price') * (F('discount') / 100.00)))).first()

        product.price_with_discount = product.annotated_price
        product.save()
