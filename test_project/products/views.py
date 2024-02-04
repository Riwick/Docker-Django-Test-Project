from django.conf import settings
from django.core.cache import cache
from django.db.models import Sum
from rest_framework.viewsets import ReadOnlyModelViewSet

from products.business_logic.controllers import get_product_queryset
from products.serializers import ProductSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = get_product_queryset()
    serializer_class = ProductSerializer

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

