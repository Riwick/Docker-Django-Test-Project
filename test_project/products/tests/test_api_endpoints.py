import json

from rest_framework.authtoken.admin import User
from django.db import connection
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test.utils import CaptureQueriesContext

from products.models import Product, Category, Seller, Profile, BasketProducts, FavoritesProducts


class ProductTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='1', first_name='1', last_name='1', password='M30012015m')
        self.seller = Seller.objects.create(company_name='1', address='1', user=self.user)
        self.category1 = Category.objects.create(name='First category')
        self.product1 = Product.objects.create(title='1', description='1',
                                               price=1200, author=self.seller, discount=0, quantity=1,
                                               category=self.category1)

        self.product2 = Product.objects.create(title='2', description='2',
                                               price=1200, author=self.seller, discount=0, quantity=1,
                                               category=self.category1)

        self.maxDiff = 20000

    def test_products_list(self):
        url = reverse('product-list')

        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(3, len(queries))

        expected_data = {
            "result": {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
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
                        'price': 1200,
                        'price_with_discount': 0,
                        'quantity': 1,
                        'discount': 0,
                        'company': '1',
                        'category_name': 'First category'
                    }
                ]
            },
            'total_price': 0
        }

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)
        self.assertEqual(response.data['result']['results'][0]['title'], '1')
        self.assertEqual(response.data['result']['results'][1]['title'], '2')
        self.assertEqual(response.data['total_price'], 0)

    def test_products_ordering(self):
        url = reverse('product-list')

        response = self.client.get(url, data={'ordering': '-title'})

        expected_data = {
            "result": {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        'title': '2',
                        'price': 1200,
                        'price_with_discount': 0,
                        'quantity': 1,
                        'discount': 0,
                        'company': '1',
                        'category_name': 'First category'
                    },
                    {
                        'title': '1',
                        'price': 1200,
                        'price_with_discount': 0,
                        'quantity': 1,
                        'discount': 0,
                        'company': '1',
                        'category_name': 'First category'
                    }
                ]
            },
            'total_price': 0
        }

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)
        self.assertEqual(response.data['result']['results'][0]['title'], '2')
        self.assertEqual(response.data['result']['results'][1]['title'], '1')
        self.assertEqual(response.data['total_price'], 0)

    def test_products_filter(self):
        url = reverse('product-list')

        response = self.client.get(url, data={'title': '1'})

        expected_data = {
            "result": {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        'title': '1',
                        'price': 1200,
                        'price_with_discount': 0,
                        'quantity': 1,
                        'discount': 0,
                        'company': '1',
                        'category_name': 'First category'
                    }
                ]
            },
            'total_price': 0
        }

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)
        self.assertEqual(response.data['result']['results'][0]['title'], '1')
        self.assertEqual(response.data['total_price'], 0)

    def test_products_search(self):
        url = reverse('product-list')

        self.user2 = User.objects.create(username='3', first_name='1', last_name='1')
        self.seller2 = Seller.objects.create(company_name='3', address='1', user=self.user2)
        self.product3 = Product.objects.create(title='3', description='3',
                                               price=1200, author=self.seller2, discount=0, quantity=3,
                                               category=self.category1)

        response = self.client.get(url, data={'search': '3'})

        expected_data = {
            "result": {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        'title': '3',
                        'price': 1200,
                        'price_with_discount': 0,
                        'quantity': 3,
                        'discount': 0,
                        'company': '3',
                        'category_name': 'First category'
                    }
                ]
            },
            'total_price': 0
        }

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)
        self.assertEqual(response.data['result']['results'][0]['title'], '3')
        self.assertEqual(response.data['total_price'], 0)

    def test_retrieve_product_view(self):

        url = reverse('product-detail', args=(self.product1.pk,))

        response = self.client.get(url)

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

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)
        self.assertEqual(response.data['title'], '1')

    def test_product_update(self):
        url = reverse('product-detail', args=(self.product1.pk,))

        data = {
            'title': '5',
            'description': '5',
            'price': 2400,
            'discount': 20,
            'quantity': 2,
        }

        json_data = json.dumps(data)
        self.client.force_login(user=self.user)

        response = self.client.put(url, data=json_data, content_type='application/json')

        print(response.data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.product1.refresh_from_db()
        self.assertEqual('5', self.product1.title)
        self.assertEqual('5', self.product1.description)
        self.assertEqual(2400, self.product1.price)
        self.assertEqual(20, self.product1.discount)
        self.assertEqual(2, self.product1.quantity)

