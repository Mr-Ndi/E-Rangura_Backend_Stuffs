from django.db import models
from Sellers.models import Seller
from Products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('decline', 'Declined'),
        ('accepted', 'Accepted'),
    ]
    order_id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.quantity and self.product_id:
            self.total_price = self.quantity * self.product_id.price
        super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.quantity > self.product_id.stock_quantity:
            raise ValidationError({
                'quantity': 'Order quantity exceeds available stock'
            })
    def __str__(self):
        return str(self.order_id)