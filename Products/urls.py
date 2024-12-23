from django.urls import path
from .views import upload_product, retrieve_product

urlpatterns = [
    path('product/', upload_product, name='upload_product'),
    path('products/', retrieve_product, name='retrive_product'),
    # path('products/<int:product_id>/', retrive_product, name='retrive_product'),
]