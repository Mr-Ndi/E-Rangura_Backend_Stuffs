from django.urls import path
from .views import order_history, order_detail

urlpatterns = [
    path('history/', order_history, name='order_history'),
    path('detail/<int:order_id>/', order_detail, name='order_detail'),
]
