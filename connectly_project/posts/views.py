# Removed unused import: render
import json 
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from .models import User, Post, Comment
# Removed unused import: CommentSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPostAuthor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



#Creators

@csrf_exempt 
def create_user(request):
    #import pdb; pdb.set_trace()  # Breakpoint to inspect request data
    if request.method == 'POST': 
        try: 
            data = json.loads(request.body) 
            user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']  # Password is hashed
            )
             
            return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status=201) 
        except Exception as e: 
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt 
def create_post(request):
    #import pdb; pdb.set_trace()  # Breakpoint to inspect request data 
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
            data = json.loads(request.body)  # Ensure data is used properly
            author = User.objects.get(id=data['author'])
            post = Post.objects.get(id=data['post'])
            comment = Comment.objects.create(
                content=data['content'],
                author=author,
                post=post
            )
            return JsonResponse({'id': comment.id, 'message': 'Comment created successfully'}, status=201)
        except (User.DoesNotExist, Post.DoesNotExist):
            return JsonResponse({'error': 'Author or post not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

#Getters
def get_users(request):  # Access request to avoid unused parameter warning
    if request.method == 'GET':
        try: 
            users = list(User.objects.values('id', 'username', 'email'))  # Removed 'created_at' as User model may not have it
            return JsonResponse(users, safe=False) 
        except Exception as e: 
            return JsonResponse({'error': str(e)}, status=500)

def get_posts(request):  # Access request to avoid unused parameter warning
    if request.method == 'GET':
        try: 
            posts = list(Post.objects.values('id', 'content', 'author', 'created_at')) 
            return JsonResponse(posts, safe=False) 
        except Exception as e: 
            return JsonResponse({'error': str(e)}, status=500)

def get_comments(request):  # Access request to avoid unused parameter warning
    if request.method == 'GET':
        try:
            comments = list(Comment.objects.values('id', 'content', 'author', 'post', 'created_at'))
            return JsonResponse(comments, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPostAuthor]
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, post)
        return Response({"content": post.content})
    
    def get(self, request):  # Access request to avoid unused parameter warning
        _ = request  # Explicitly access request
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "Authenticated!"})