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