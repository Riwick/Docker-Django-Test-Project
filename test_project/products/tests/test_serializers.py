from django.test import TestCase
from djoser.conf import User

from products.models import Product, Category, Seller, Profile, BasketProducts, FavoritesProducts
from products.serializers import ProductSerializer, DetailProductSerializer, SellerSerializer, SellerObjectSerializer, \
    CategorySerializer, ProfileSerializer, BasketProductsSerializer, BasketObjectSerializer, \
    FavoritesProductsSerializer, FavoritesProductsObjectSerializer


class ProductSerializerTestCase(TestCase):

    def test_products(self):
        user = User.objects.create(username='1', first_name='1', last_name='1')
        seller = Seller.objects.create(company_name='1', address='1', user=user)
        category1 = Category.objects.create(name='First category')
        product1 = Product.objects.create(title='1', description='1',
                                          price=1200, author=seller, discount=0, quantity=1, category=category1)
        Product.objects.create(title='2', description='2',
                               price=2000, author=seller, discount=0, quantity=1, category=category1)

        products = Product.objects.all()

        data1 = ProductSerializer(products, many=True).data

        expected_data = [
            {
                'title': '1',
                'price': 1200,
                'price_with_discount': 0,
                'quantity': 1,
                'discount': 0,
                'company': '1',
                'category_name': 'First category'
            },
            {
                'title': '2',
                'price': 2000,
                'price_with_discount': 0,
                'quantity': 1,
                'discount': 0,
                'company': '1',
                'category_name': 'First category'
            }
        ]

        self.assertEqual(expected_data, data1)

        # test ProductDetailSerializer

        data2 = DetailProductSerializer(product1).data

        expected_data = {
            'title': '1',
            'description': '1',
            'price': 1200,
            'price_with_discount': 0,
            'discount': 0,
            'quantity': 1,
            'category_name': 'First category',
            'company_name': '1'
        }

        self.assertEqual(expected_data, data2)


class SellerSerializerTestCase(TestCase):

    def test_sellers(self):
        user = User.objects.create(username='1', first_name='1', last_name='1')
        seller1 = Seller.objects.create(company_name='1', address='1', user=user)
        Seller.objects.create(company_name='2', address='2', user=user)

        sellers = Seller.objects.all()

        data = SellerSerializer(sellers, many=True).data

        expected_data = [
            {
                'company_name': '1',
                'address': '1',
                'user_username': '1'
            },
            {
                'company_name': '2',
                'address': '2',
                'user_username': '1'
            }
        ]

        self.assertEqual(expected_data, data)

        # test SellerObjectSerializer

        data = SellerObjectSerializer(seller1).data

        time_created = data.get('date_joined')
        expected_data = {
            'id': 4,
            'company_name': '1',
            'user_username': '1',
            'address': '1',
            'date_joined': time_created
        }

        self.assertEqual(expected_data, data)


class CategorySerializerTestCase(TestCase):

    def test_category(self):
        Category.objects.create(name='First category')
        Category.objects.create(name='Second category')

        categories = Category.objects.all()

        data = CategorySerializer(categories, many=True).data

        expected_data = [
            {
                'name': 'First category',
            },
            {
                'name': 'Second category',
            }
        ]

        self.assertEqual(expected_data, data)


class ProfileSerializerTestCase(TestCase):

    def test_profile(self):
        user1 = User.objects.create(username='1', first_name='1', last_name='1')
        user2 = User.objects.create(username='2', first_name='2', last_name='2')
        Profile.objects.create(user=user1)
        Profile.objects.create(user=user2)

        profiles = Profile.objects.all()

        data = ProfileSerializer(profiles, many=True).data

        expected_data = [
            {
                'profile_username': '1',
                'profile_first_name': '1',
                'profile_last_name': '1',
                'profile_email': ''
            },
            {
                'profile_username': '2',
                'profile_first_name': '2',
                'profile_last_name': '2',
                'profile_email': ''
            }
        ]

        self.assertEqual(expected_data, data)


class BasketProductsSerializerTestCase(TestCase):

    def test_basket(self):
        user1 = User.objects.create(username='1', first_name='1', last_name='1')
        seller = Seller.objects.create(company_name='1', address='1', user=user1)
        category1 = Category.objects.create(name='First category')
        product1 = Product.objects.create(title='1', description='1',
                                          price=1200, author=seller, discount=0, quantity=1, category=category1)

        basket_1 = BasketProducts.objects.create(user=user1, product=product1)
        BasketProducts.objects.create(user=user1, product=product1)

        baskets = BasketProducts.objects.all()

        data = BasketProductsSerializer(baskets, many=True).data

        expected_data = [
            {
                'id': 1,
                'quantity': 1,
                'basket_product': '1',
                'basket_price_with_discount': 0,
                'basket_user': '1',
                'product': 1,
                'user': 1
            },
            {
                'id': 2,
                'quantity': 1,
                'basket_product': '1',
                'basket_price_with_discount': 0,
                'basket_user': '1',
                'product': 1,
                'user': 1
            }
        ]

        self.assertEqual(expected_data, data)

        # test BasketObjectSerializer

        data = BasketObjectSerializer(basket_1).data

        expected_data = {
                'id': 1,
                'quantity': 1,
                'product': 1,
                'basket_price_with_discount': 0,
                'user': 1
            }

        self.assertEqual(expected_data, data)


class FavoritesProductsSerializerTestCase(TestCase):

    def test_favorites(self):
        user1 = User.objects.create(username='1', first_name='1', last_name='1')
        seller = Seller.objects.create(company_name='1', address='1', user=user1)
        category1 = Category.objects.create(name='First category')
        product1 = Product.objects.create(title='1', description='1',
                                          price=1200, author=seller, discount=0, quantity=1, category=category1)

        favorite = FavoritesProducts.objects.create(user=user1, product=product1)
        FavoritesProducts.objects.create(user=user1, product=product1)

        favorites = FavoritesProducts.objects.all()

        data = FavoritesProductsSerializer(favorites, many=True).data

        expected_data = [
            {
                'id': 1,
                'product_title': '1',
                'user_name': '1',
                'product': 2,
                'user': 2
            },
            {
                'id': 2,
                'product_title': '1',
                'user_name': '1',
                'product': 2,
                'user': 2
            }
        ]

        self.assertEqual(expected_data, data)

        # test FavoritesProductsObjectSerializer

        data1 = FavoritesProductsObjectSerializer(favorite).data

        expected_data = {
            'id': 1,
            'user': 2,
            'product': 2
        }

        self.assertEqual(expected_data, data1)