from django.urls import path
from .views import create_seller

urlpatterns = [
    path('create-seller/', create_seller, name='create_seller')
]