from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_posts, name='get_posts'),
    path('create/', views.create_post, name='create_post'),
    path('users/', views.get_users, name='get_users'),
    path('users/create/', views.create_user, name='create_user'),
]
