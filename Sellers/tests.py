from django.test import TestCase
from .models import Seller
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import json

class SellerModelTest(TestCase):

    def test_seller_string_representation(self):
        seller = Seller.objects.create(
            names="Ninshuti Poli Ndiramiye",
            email="ndiramiyeninshuti1@gmail.com",
            password="securepassword#123",
            district="Nyarugenge",
            sector="Rwampara",
            telephone="0791332245",
            username="Mr Ndi"
        )
        self.assertEqual(str(seller), "Ninshuti Poli Ndiramiye")

    def test_username_field_max_length(self):
        seller = Seller(username='U' * 3) # setting the username to 33 characters
        with self.assertRaises(Exception):
            seller.full_clean()

    def test_invalid_email(self):
        seller = Seller(email="invalid_email_address")
        with self.assertRaises(Exception):
            seller.full_clean()

class NewSellerViewTest(TestCase):

    def setUp(self):
        self.username = 'Ndi'
        self.password = 'test Ndi'
        self.email = 'ndiramiyeninshuti1@gmail.com'
        self.user = Seller.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email
        )
        self.token = Token.objects.create(user=self.user)

    def test_create_seller_success(self):
        url = reverse('create_seller')
        data = {
            "names": "Ninshuti Poli Ndiramiye",
            "email": "ndiramiyeninshuti13@gmail.com",
            "password": "securepassword#123",
            "district": "Nyarugenge",
            "sector": "Rwampara",
            "telephone": "0791332245",
            "username": "Mr Ndi2"
        }
        initial_count = Seller.objects.count()
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )
        # print(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Seller.objects.count(), initial_count + 1)
        new_seller = Seller.objects.get(email='ndiramiyeninshuti13@gmail.com')
        self.assertEqual(new_seller.names, "Ninshuti Poli Ndiramiye")

class UserLoginTest(TestCase):
    def setUp(self):
        self.username = 'Ndi'
        self.password = 'test Ndi'
        self.email = 'ndiramiyeninshuti2@gmail.com'
        self.user = Seller.objects.create_user(username=self.username, password=self.password, email=self.email)
        self.token = Token.objects.create(user=self.user)

    def test_login_success(self):
        url = reverse('login_user')
        data = {
            "username": self.username,
            "password": self.password
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login succesfull', response.json().get('message'))

    def test_login_failue(self):
        url = reverse('login_user')
        data = {
            "username": self.username,
            "password": "wrongpassword"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid credentials', response.json().get('error'))