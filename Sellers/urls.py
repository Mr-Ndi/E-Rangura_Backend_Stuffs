from django.urls import path
from .views import create_seller,login_user, logout_user

urlpatterns = [
    path('create-seller/', create_seller, name='create_seller'),
    path('login/',login_user, name='login_user'),
     path('logout/', logout_user, name='logout'),
]