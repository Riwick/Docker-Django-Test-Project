from django.conf import settings
from django.contrib.auth import logout
from django.core.cache import cache
from django.db.models import Sum
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet


from products.business_logic.controllers import get_product_queryset, get_seller_queryset, get_detail_product_queryset
from products.permissions import IsAuthorOrReadOnly, IsAdminOrStaffOrReadOnly
from products.serializers import ProductSerializer, SellerSerializer, DetailProductSerializer


class ProductsPaginator(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    max_page_size = 2


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = get_product_queryset()
    serializer_class = ProductSerializer
    pagination_class = ProductsPaginator
    authentication_classes = [SessionAuthentication, BasicAuthentication]

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


class UpdateDeleteProductView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_detail_product_queryset()
    lookup_field = 'id'
    serializer_class = DetailProductSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAdminOrStaffOrReadOnly]


class SellerProfileViewSet(ReadOnlyModelViewSet):
    queryset = get_seller_queryset()
    serializer_class = SellerSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


