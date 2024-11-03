from django.urls import path
from .views import upload_product

urlpatterns = [
    path('upload/', upload_product, name='upload_product'),
    path('products/', product_list, name='product_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
]
