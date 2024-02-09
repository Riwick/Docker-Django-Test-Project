from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin, \
    CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from products.models import BasketProducts, FavoritesProducts, Product, Seller


class BasketCreateListView(CreateModelMixin,
                           ListModelMixin,
                           GenericViewSet):

    def list(self, request, *args, **kwargs):
        queryset = BasketProducts.objects.filter(user_id=self.request.user.id).select_related('product', 'user')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FavoritesProductsCreateListViewSet(CreateModelMixin,
                                         ListModelMixin,
                                         GenericViewSet):

    def list(self, request, *args, **kwargs):
        queryset = FavoritesProducts.objects.filter(user_id=self.request.user.id).select_related('product', 'user')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SellerProductsListUpdateDeleteViewSet(ListModelMixin,
                                            GenericViewSet):

    def list(self, request, *args, **kwargs):
        queryset = (Product.objects.filter(author_id=self.request.query_params.get('id')).
                    select_related('category', 'author'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
