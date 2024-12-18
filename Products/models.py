from django.db import models
from Sellers.models import Sellers

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    price = models.DecimalField()
    stock_quantity = models.IntegerField()
    unit = models.CharField(max_length=3)
    minimum_for_deliver = models.IntegerField()
    description = models.CharField(min_length=10, max_length=200)
    owner_id = models.ForeignKey(sellers, on_delete=models.CASCADE)

    def __str__(self):
        return self.name