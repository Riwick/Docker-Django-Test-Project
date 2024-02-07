from django.contrib import admin

from products.models import Product, Seller, Category, BasketProducts, Profile, FavoritesProducts

admin.site.register(Product)
admin.site.register(Seller)
admin.site.register(Category)
admin.site.register(BasketProducts)
admin.site.register(Profile)
admin.site.register(FavoritesProducts)
