from django.urls import path
from .views import create_order, retrieve_user_orders, filter_user_orders

urlpatterns = [
    path('create/', create_order, name='create-order'),
    path('all/', retrieve_user_orders, name='retrieve-user-orders'),
    path('filter/', filter_user_orders, name='filter-user-orders'),
]
