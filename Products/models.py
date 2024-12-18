from django.db import models
from Sellers.models import Seller

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    stock_quantity = models.IntegerField()
    unit = models.CharField(max_length=3)
    minimum_for_deliver = models.IntegerField()
    description = models.CharField(max_length=200)
    owner_id = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return self.name