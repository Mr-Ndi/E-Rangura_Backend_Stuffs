from django.urls import path
from .views import (
    upload_product,
    product_list,
    product_detail,
    update_product,
    delete_product,
    my_product_list
)

urlpatterns = [
    path('upload/', upload_product, name='upload_product'),
    path('products/', product_list, name='product_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('products/update/<int:product_id>/', update_product, name='update_product'),
    path('products/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('my-products/', my_product_list, name='my_product_list'),
]
