from django.db import models

class Sellers(models.Model):
    seller_id = models.IntegerField(primary_key=True)
    names = models.CharField(max_length=32)
    email = model.EmailField()
    password = models.CharField(max_length=32)
    district = models.CharField(max_length=32)
    sector = models.CharField(max_length=32)
    telephone = models.CharField(max_length=13)
    username = models.CharField(max_length=32)

    def __str__(self):
        return self.names