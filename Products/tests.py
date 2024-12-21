import json
from django.urls import reverse
from .models import Product
from django.test import TestCase
from Sellers.models import Seller
from rest_framework.authtoken.models import Token


class ProductModeltesting(TestCase):
    def setUp(self):
        self.username = 'Ndi'
        self.password = 'password for testing'
        self.email = 'ndiramiyeninshuti1@gmail.com'
        self.seller = Seller.objects.create(username=self.username, password=self.password, email=self.email)
        self.token = Token.objects.create(user=self.seller)

    def test_product_string_representation(self):
        product = Product.objects.create(
            name="Sample Product",
            price=1000,
            stock_quantity=1000,
            unit="kg",
            minimum_for_deliver=700,
            description="A sample of description for the sample product",
            owner_id=self.seller
        )
        self.assertEqual(str(product), "Sample Product")


class ProductCreationTest(TestCase):
    def create_product(self):
        url = reverse('upload_product')
        data = {
            "name": "Sample Product",
            "price": 1000,
            "stock_quantity": 1000,
            "unit": "kg",
            "minimum_for_deliver": 700,
            "description":"A sample of description for the sample product",
            "owner": self.seller.id
        }
        response = self.client.post(
            url,
            data = json.dumps(data),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer '+ self.token.key
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('Product created successfully!', response.json.get('message'))
    
    def test_create_product_without_authentication(self):
        url = reverse('upload_product')
        data={
            "name": "Sample Product",
            "price": 1000,
            "stock_quantity": 1000,
            "unit": "kg",
            "minimum_for_deliver": 700,
            "description":"A sample of description for the sample product",
        }
        response = self.client.post(
            url,
            data = json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)


class ProductRetrivalTest(TestCase):
    def setUp(self):
        self.seller = Seller.objects.create_user(
            username='testUser',
            password='testpass123',
            email='test@example.com',
            names='uwo kwifashishwa',
            district='Nyarugenge',
            sector='Rwampara',
            telephone='0792334455'
        )

        self.product1 = Product.objects.create(
            name="Test Product 1",
            price=1000,
            stock_quantity=50,
            unit="kg",
            minimum_for_deliver=5,
            description="Test description 1",
            owner_id=self.seller
        )
        
        self.product2 = Product.objects.create(
            name="Test Product 2",
            price=2000,
            stock_quantity=100,
            unit="pieces",
            minimum_for_deliver=10,
            description="Test description 2",
            owner_id=self.seller
        )

    def test_retrive_all_products(self):
        url = reverse('retrice_product')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['products']), 2)
        self.assertEqual(data['message'], 'Product retrived succesfully')
