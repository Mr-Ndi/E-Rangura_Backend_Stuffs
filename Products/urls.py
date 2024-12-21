from django.urls import path
from .views import upload_product

urlpatterns = [
    path('upload_product/', upload_product, name='upload_product')
]