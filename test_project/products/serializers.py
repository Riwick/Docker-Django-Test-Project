from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from products.models import Product, Seller, Category, BasketProducts, Profile


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


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class ProfileSerializer(ModelSerializer):
    profile_username = serializers.CharField(source='username')
    profile_first_name = serializers.CharField(source='first_name')
    profile_last_name = serializers.CharField(source='last_name')
    profile_email = serializers.CharField(source='email', read_only=True)

    class Meta:
        model = Profile
        fields = ('profile_username', 'profile_first_name', 'profile_last_name', 'profile_email')


class BasketProductsSerializer(ModelSerializer):
    price_with_discount = serializers.IntegerField(source='product.price_with_discount', read_only=True)

    class Meta:
        model = BasketProducts
        fields = ('id', 'quantity', 'product', 'price_with_discount', 'product', 'user')


class BasketObjectSerializer(ModelSerializer):
    price_with_discount = serializers.IntegerField(source='product.price_with_discount', read_only=True)

    class Meta:
        model = BasketProducts
        fields = ('id', 'quantity', 'product', 'price_with_discount', 'product', 'user')
