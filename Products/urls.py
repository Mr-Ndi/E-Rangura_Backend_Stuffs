from django.urls import path
from .views import upload_product, retrive_product

urlpatterns = [
    path('product/', upload_product, name='upload_product'),
    path('products/', retrive_product, name='retrive_product'),
    path('products/<int:product_id>/', retrive_product, name='retrive_product'),
]