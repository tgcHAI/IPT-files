from django.urls import path
from .views import UserListCreate, PostListCreate, CommentListCreate

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('users/create/', UserListCreate.as_view(), name='user-list-create'),  # if separate endpoint is desired
    path('posts/', PostListCreate.as_view(), name='post-list-create'),
    path('posts/create/', PostListCreate.as_view(), name='post-list-create'),
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
]