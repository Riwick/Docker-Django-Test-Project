from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from products.models import Product


class ProductSerializer(ModelSerializer):
    company = serializers.CharField(source='author.company_name')
    price = serializers.SerializerMethodField()

    def get_price(self, instance):
        return instance.price

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'discount', 'company')
