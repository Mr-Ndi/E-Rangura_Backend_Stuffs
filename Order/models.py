from django.db import models
from Sellers.models import Seller
from Products.models import Product

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('decline', 'Declined'),
        ('accepted', 'Accepted'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES) #for holding pending,declined or accepted

    def __str__(self):
        return str(self.order_id)