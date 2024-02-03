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

        total_price = queryset.aggregate(total=Sum('price')).get('total')

        response.data = {'result': response.data, 'total_price': total_price}
        return response
