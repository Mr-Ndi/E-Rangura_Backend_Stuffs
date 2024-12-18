from django.db import models

class Seller(models.Model):
    seller_id = models.AutoField(primary_key=True)
    names = models.CharField(max_length=32)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    district = models.CharField(max_length=32)
    sector = models.CharField(max_length=32)
    telephone = models.CharField(max_length=13)
    username = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.names