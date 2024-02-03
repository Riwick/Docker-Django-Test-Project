from django.db.models import F

from products.models import Product


def get_product_queryset():
    return (Product.objects.all().
            only('title', 'description', 'author__company_name', 'price', 'discount'))
