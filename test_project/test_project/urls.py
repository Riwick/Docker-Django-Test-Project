from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from products.views import ProductViewSet, SellersProfileViewSet, RetrieveUpdateDeleteProductView, CategoryViewSet, \
    ProfileView, BasketViewSet, BasketObjectView, FavoritesProductsViewSet, FavoritesProductsObjectView, \
    CreateProductView, SellerProfileObjectView, SellerProductsListView, AddCategoryView

router = routers.SimpleRouter()

router.register(r'products', ProductViewSet)
router.register(r'sellers', SellersProfileViewSet, basename='Seller')
router.register(r'category', CategoryViewSet, basename='Category')
router.register(r'basket', BasketViewSet, basename='Basket')
router.register(r'favorites_products', FavoritesProductsViewSet, basename='FavoritesProducts')
router.register(r'seller-products', SellerProductsListView, basename='SellerProducts')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/<int:id>/', RetrieveUpdateDeleteProductView.as_view(), name='product-detail'),
    path('product_add/', CreateProductView.as_view(), name='create-product'),

    path('category_add/', AddCategoryView.as_view(), name='create-category'),

    path('accounts/profile/<int:id>/', ProfileView.as_view(), name='profile'),
    path('basket/<int:id>/', BasketObjectView.as_view(), name='basket-detail'),
    path('favorites_products/<int:id>/', FavoritesProductsObjectView.as_view(), name='favorites-products-detail'),

    path('seller-profile/', SellerProfileObjectView.as_view(), name='seller-profile'),
    path('profile/<int:id>/', ProfileView.as_view(), name='user-profile'),

    re_path('social_auth/', include('social_django.urls', namespace='social')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
]

urlpatterns += router.urls
