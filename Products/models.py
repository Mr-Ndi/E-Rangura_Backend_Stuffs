from django.db import models
from Sellers import Sellers

class Product(models.Model):
    product_id = models.AutoFiels(primary_key=True)
    name = models.ChatField(max_length=20)
    price = models.decimalField()
    stock_quantity = models.integerField()
    unit = models.stringField(min_length=2, max_length=3)
    minimum_for_deliver = models.integerField()
    description = models.CharField(min_length=10, max_length=200)
    owner_id = models.ForeignKey(sellers, on_delete=models.CASCADE)

    def __str__(self):
        return self.name