from django.db.models import F


def get_product_queryset():
    from products.models import Product
    return (Product.objects.all().
            select_related('author', 'category'))

