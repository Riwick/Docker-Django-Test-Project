from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from products.models import Product, Seller, Category, BasketProducts, Profile, FavoritesProducts


class ProductSerializer(ModelSerializer):
    company = serializers.CharField(source='author.company_name')
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ('title', 'price', 'price_with_discount', 'discount', 'company', 'category_name')


class DetailProductSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category_name = serializers.CharField(source='category.name', read_only=True)
    company_name = serializers.CharField(source='author.company_name', read_only=True)

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'price_with_discount', 'discount', 'quantity', 'category_name',
                  'company_name', 'user')

        read_only_fields = ('price_with_discount',)


class CreateProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'price_with_discount', 'discount', 'quantity', 'author', 'category', )
        read_only_fields = ('price_with_discount',)


class SellerSerializer(ModelSerializer):
    user_username = serializers.CharField(source='user.username')

    class Meta:
        model = Seller
        fields = ('company_name', 'address', 'user_username')


class SellerObjectSerializer(ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)

    class Meta:
        model = Seller
        fields = ('id', 'company_name', 'user_username', 'address', 'date_joined')


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
    basket_price_with_discount = serializers.IntegerField(source='product.price_with_discount', read_only=True)
    basket_product = serializers.CharField(source='product.title', read_only=True)
    basket_user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = BasketProducts
        fields = ('id', 'quantity', 'basket_product', 'basket_price_with_discount', 'basket_user', 'product', 'user')


class BasketObjectSerializer(ModelSerializer):
    basket_price_with_discount = serializers.IntegerField(source='product.price_with_discount', read_only=True)

    class Meta:
        model = BasketProducts
        fields = ('id', 'quantity', 'product', 'basket_price_with_discount', 'user')


class FavoritesProductsSerializer(ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = FavoritesProducts
        fields = ('id', 'product_title', 'user_name', 'product', 'user')


class FavoritesProductsObjectSerializer(ModelSerializer):

    class Meta:
        model = FavoritesProducts
        fields = '__all__'
