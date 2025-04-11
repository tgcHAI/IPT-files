# posts/views.py (Clean & Fixed for Activity 9–10 Completion)

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .permissions import IsPostAuthor
from .serializations import CommentSerializer


#Creators
@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            author = User.objects.get(id=data['author'])
            post = Post.objects.create(content=data['content'], author=author)
            return JsonResponse({'id': post.id, 'message': 'Post created successfully'}, status=201)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Author not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def create_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            author = User.objects.get(id=data['author'])
            post = Post.objects.get(id=data['post'])
            comment = Comment.objects.create(
                content=data['content'], author=author, post=post
            )
            return JsonResponse({'id': comment.id, 'message': 'Comment created successfully'}, status=201)
        except (User.DoesNotExist, Post.DoesNotExist):
            return JsonResponse({'error': 'Author or post not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# Getters
def get_users(request):
    try:
        users = list(User.objects.values('id', 'username', 'email', 'date_joined'))
        return JsonResponse(users, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_posts(request):
    try:
        posts = list(Post.objects.values('id', 'content', 'author', 'created_at'))
        return JsonResponse(posts, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_comments(request):
    try:
        comments = list(Comment.objects.values('id', 'content', 'author', 'post', 'created_at'))
        return JsonResponse(comments, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



#Specific
class PostDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, post)
        return Response({"content": post.content})
