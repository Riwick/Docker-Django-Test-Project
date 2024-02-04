

def get_product_queryset():
    from products.models import Product
    return (Product.objects.all().
            select_related('author', 'category'))


def get_detail_product_queryset():
    from products.models import Product
    return Product.objects.all().select_related('author', 'author', 'category')


def get_seller_queryset():
    from products.models import Seller
    return Seller.objects.all().select_related('user').only('company_name', 'address', 'user__username')
