from django.test import TestCase
from .models import Seller

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

