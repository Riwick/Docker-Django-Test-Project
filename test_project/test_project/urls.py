from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from products.views import ProductViewSet, SellersProfileViewSet, RetrieveUpdateDeleteProductView, CategoryViewSet, ProfileView

router = routers.SimpleRouter()

router.register(r'products', ProductViewSet, basename='Products')
router.register(r'sellers', SellersProfileViewSet, basename='Seller')
router.register(r'category', CategoryViewSet, basename='Category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/<int:id>/', RetrieveUpdateDeleteProductView.as_view(), name='Product-detail'),
    path('accounts/profile/<int:id>/', ProfileView.as_view(), name='profile'),

    re_path('social_auth/', include('social_django.urls', namespace='social')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
]

urlpatterns += router.urls
