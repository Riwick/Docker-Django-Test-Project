def get_product_queryset():
    from products.models import Product
    return Product.objects.all().select_related('author', 'category')


def get_seller_queryset():
    from products.models import Seller
    return Seller.objects.all().select_related('user').only('company_name',
                                                            'address', 'user__username', 'user__date_joined')


def get_category_queryset():
    from products.models import Category
    return Category.objects.all()


def get_profile_queryset():
    from products.models import Profile
    return Profile.objects.all()


def get_basket_queryset():
    from products.models import BasketProducts
    return BasketProducts.objects.all().select_related('product', 'user')


def get_favorites_products_queryset():
    from products.models import FavoritesProducts
    return FavoritesProducts.objects.all().select_related('product', 'user')
