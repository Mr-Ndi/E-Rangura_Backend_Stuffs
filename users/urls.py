from django.urls import path
from .views import register_user, login_user, list_users, get_user

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('users/', list_users, name='list_users'), 
    path('users/<int:user_id>/', get_user, name='get_user'), 
]