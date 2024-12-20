from django.test import TestCase
from .models import Seller
from django.contrib.auth.models import User
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
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)

    def test_create_seller_success(self):
        url = reverse('create_seller')
        data = {
            "names": "Ninshuti Poli Ndiramiye",
            "email": "ndiramiyeninshuti1@gmail.com",
            "password": "securepassword#123",
            "district": "Nyarugenge",
            "sector": "Rwampara",
            "telephone": "0791332245",
            "username": "Mr Ndi"
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Seller.objects.count(), 1)
        self.assertEqual(Seller.objects.get().names, "Ninshuti Poli Ndiramiye")