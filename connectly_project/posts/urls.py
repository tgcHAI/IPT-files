from django.urls import path 
from . import views 
 
urlpatterns = [ 
    path('users/', views.get_users, name='get_users'), 
    path('users/create/', views.create_user, name='create_user'), 
    path('posts/', views.get_posts, name='get_posts'), 
    path('posts/create/', views.create_post, name='create_post'),
    path('comments/', views.get_comments, name='get_comments'),
    path('comments/create/', views.create_comment, name='create_comment'),
 
]