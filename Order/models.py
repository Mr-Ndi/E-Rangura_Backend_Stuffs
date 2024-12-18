from django.db import models
from Seller.models import Seller
from Prodects.models import Product

class Order(models.Model):
    order_id = models.AutoField(primmary_key=True)
    owner_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(max_length=20)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('decline', 'Declined'),
        ('accepted', 'Accepted'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES) #for holding pending,declined or accepted

    def __str__(self):
        return str(self.order_id)