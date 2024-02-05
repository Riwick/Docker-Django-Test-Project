from django.conf import settings
from django.contrib.auth import logout
from django.core.cache import cache
from django.db.models import Sum, Count
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet


from products.business_logic.controllers import get_product_queryset, get_seller_queryset, get_detail_product_queryset, \
    get_category_queryset, get_user_queryset
from products.permissions import IsAuthorOrReadOnly, IsAdminOrStaffOrReadOnly, IsUserOrSuperUserOrStaffOrReadOnly
from products.serializers import ProductSerializer, SellerSerializer, DetailProductSerializer, CategorySerializer, \
    ProfileSerializer


class ProductsPaginator(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    max_page_size = 2


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = get_product_queryset()
    serializer_class = ProductSerializer
    pagination_class = ProductsPaginator

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(self, request, *args, **kwargs)

        price_cache = cache.get(settings.PRICE_CACHE_NAME)

        if price_cache:
            total_price = price_cache
        else:
            total_price = queryset.aggregate(total=Sum('price')).get('total')
            cache.set(settings.PRICE_CACHE_NAME, total_price, 60 * 60)

        response_data = {'result': response.data, 'total_price': total_price}
        response.data = response_data
        return response


class RetrieveUpdateDeleteProductView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_detail_product_queryset()
    lookup_field = 'id'
    serializer_class = DetailProductSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAdminOrStaffOrReadOnly, IsAuthenticated]


class SellersProfileViewSet(ReadOnlyModelViewSet):
    queryset = get_seller_queryset()
    serializer_class = SellerSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = get_category_queryset()
    serializer_class = CategorySerializer

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

