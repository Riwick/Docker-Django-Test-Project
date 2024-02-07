from django.contrib import admin

from products.models import Product, Seller, Category, BasketProducts, Profile

admin.site.register(Product)
admin.site.register(Seller)
admin.site.register(Category)
admin.site.register(BasketProducts)
admin.site.register(Profile)
