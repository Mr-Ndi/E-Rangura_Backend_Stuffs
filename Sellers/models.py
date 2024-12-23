from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class SellerManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        if not email:
            raise ValueError('Email is required')
            
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

class Seller(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    names = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    district = models.CharField(max_length=32)
    sector = models.CharField(max_length=32)
    telephone = models.CharField(max_length=13)
    username = models.CharField(max_length=32, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=False)

    objects = SellerManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'names']

    def __str__(self):
        return self.names