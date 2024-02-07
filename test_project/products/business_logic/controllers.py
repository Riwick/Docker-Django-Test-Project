


def get_product_queryset():
    from products.models import Product
    return Product.objects.all().select_related('author', 'category')


def get_detail_product_queryset():
    from products.models import Product
    return Product.objects.all().select_related('author', 'category')


def get_seller_queryset():
    from products.models import Seller
    return Seller.objects.all().select_related('user').only('company_name', 'address', 'user__username')


def get_category_queryset():
    from products.models import Category
    return Category.objects.all()


def get_user_queryset():
    from django.contrib.auth.models import User
    return User.objects.all()


def get_basket_queryset():
    from products.models import BasketProducts
    return BasketProducts.objects.all().select_related('product', 'user')