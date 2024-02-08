from django.conf import settings
from django.core.cache import cache
from django.db.models import Sum, Count
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from products.business_logic.controllers import get_product_queryset, get_seller_queryset, \
    get_category_queryset, get_user_queryset, get_basket_queryset, get_favorites_products_queryset
from products.custom_viewsets import BasketCreateListView, FavoritesProductsCreateListViewSet
from products.models import BasketProducts, FavoritesProducts, Product
from products.permissions import IsAuthorOrReadOnly, IsAdminOrStaffOrReadOnly, IsUserOrSuperUserOrStaffOrReadOnly, \
    IsOwnerOrReadOnly, IsSellerOrReadOnly
from products.serializers import ProductSerializer, SellerSerializer, DetailProductSerializer, CategorySerializer, \
    ProfileSerializer, BasketProductsSerializer, BasketObjectSerializer, FavoritesProductsSerializer, \
    FavoritesProductsObjectSerializer, CreateProductSerializer, SellerObjectSerializer


class Paginator(PageNumberPagination):
    page_size = 4
    page_query_param = 'page'
    max_page_size = 2


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = get_product_queryset()
    serializer_class = ProductSerializer
    pagination_class = Paginator
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['title', 'price', 'category', 'author__company_name']
    search_fields = ['title', 'description', '=price', 'author__company_name', 'discount']
    filterset_fields = ['title', 'price', 'author__company_name', 'discount']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(self, request, *args, **kwargs)

        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price_with_discount')).get('total')
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60 * 60)

        response_data = {'result': response.data, 'total_price': total_price}
        response.data = response_data
        return response


class RetrieveUpdateDeleteProductView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_product_queryset()
    lookup_field = 'id'
    serializer_class = DetailProductSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAdminOrStaffOrReadOnly]


class CreateProductView(generics.CreateAPIView):
    queryset = get_product_queryset()
    serializer_class = CreateProductSerializer
    permission_classes = [IsAuthenticated]


class SellersProfileViewSet(ReadOnlyModelViewSet):
    queryset = get_seller_queryset()
    serializer_class = SellerSerializer
    pagination_class = Paginator


class SellerProfileObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_seller_queryset()
    lookup_field = 'id'
    serializer_class = SellerObjectSerializer
    permission_classes = [IsSellerOrReadOnly]


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = get_category_queryset()
    serializer_class = CategorySerializer
    pagination_class = Paginator

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(self, request, *args, **kwargs)

        category_cache = cache.get(settings.CATEGORY_CACHE_NAME)

        if category_cache:
            total_count = category_cache
        else:
            total_count = queryset.aggregate(Total=Count('name')).get('Total')
            cache.set(settings.CATEGORY_CACHE_NAME, total_count, 60 * 60)

        response_data = {'result': response.data, 'total_count': total_count}
        response.data = response_data

        return response


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = get_user_queryset()
    lookup_field = 'id'
    serializer_class = ProfileSerializer
    permission_classes = [IsUserOrSuperUserOrStaffOrReadOnly, IsAuthenticated]


class BasketViewSet(BasketCreateListView):
    pagination_class = Paginator
    serializer_class = BasketProductsSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = BasketProducts.objects.filter(user_id=self.request.user.id).select_related('product', 'user')
        response = super().list(self, request, *args, **kwargs)

        total_price = cache.get(settings.BASKET_TOTAL_PRICE_NAME)

        if total_price:
            total_sum = total_price
        else:
            total_sum = queryset.aggregate(total=Sum('product__price_with_discount')).get('total')
            cache.set(settings.BASKET_TOTAL_PRICE_NAME, total_sum, 60 * 60)

        response_data = {'result': response.data, 'total_sum': total_sum}
        response.data = response_data

        return response


class BasketObjectView(generics.RetrieveDestroyAPIView):
    queryset = get_basket_queryset()
    lookup_field = 'id'
    serializer_class = BasketObjectSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]


class FavoritesProductsViewSet(FavoritesProductsCreateListViewSet):
    queryset = get_favorites_products_queryset()
    pagination_class = Paginator
    serializer_class = FavoritesProductsSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = FavoritesProducts.objects.filter(user_id=self.request.user.id).select_related('product', 'user')
        response = super().list(self, request, *args, **kwargs)

        total_count = cache.get(settings.FAVORITES_PRODUCTS_CACHE_NAME)

        if total_count:
            count = total_count
        else:
            count = queryset.aggregate(total=Count('product')).get('total')
            cache.set(settings.FAVORITES_PRODUCTS_CACHE_NAME, count, 60 * 60)

        response_data = {'result': response.data, 'total_count': count}
        response.data = response_data

        return response


class FavoritesProductsObjectView(generics.RetrieveDestroyAPIView):
    queryset = get_favorites_products_queryset()
    lookup_field = 'id'
    serializer_class = FavoritesProductsObjectSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
