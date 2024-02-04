from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from products.models import Product


class ProductSerializer(ModelSerializer):
    company = serializers.CharField(source='author.company_name')
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ('title', 'price', 'price_with_discount', 'discount', 'company', 'category_name')
