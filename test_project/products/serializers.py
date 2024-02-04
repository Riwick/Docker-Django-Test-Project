from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from products.models import Product, Seller


class ProductSerializer(ModelSerializer):
    company = serializers.CharField(source='author.company_name')
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ('title', 'price', 'price_with_discount', 'discount', 'company', 'category_name')


class SellerSerializer(ModelSerializer):
    user_username = serializers.CharField(source='user.username')

    class Meta:
        model = Seller
        fields = ('company_name', 'address', 'user_username')


class DetailProductSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category_name = serializers.CharField(source='category.name', read_only=True)
    company_name = serializers.CharField(source='author.company_name', read_only=True)

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'price_with_discount', 'discount', 'quantity', 'category_name',
                  'company_name', 'user')

        read_only_fields = ('price_with_discount',)
