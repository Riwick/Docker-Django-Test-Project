from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from products.views import ProductViewSet, SellerProfileViewSet, UpdateDeleteProductView
router = routers.SimpleRouter()

router.register(r'products', ProductViewSet, basename='Products')
router.register(r'sellers', SellerProfileViewSet, basename='Seller')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('products/<int:id>/', UpdateDeleteProductView.as_view()),
]

urlpatterns += router.urls
