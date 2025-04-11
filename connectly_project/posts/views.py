from django.shortcuts import render
import json 
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt 
from .models import User, Post

#Creators

@csrf_exempt 
def create_user(request):
    import pdb; pdb.set_trace()  # Breakpoint to inspect request data
    if request.method == 'POST': 
        try: 
            data = json.loads(request.body) 
            user = User.objects.create(username=data['username'], email=data['email']) 
            return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status=201) 
        except Exception as e: 
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt 
def create_post(request):
    import pdb; pdb.set_trace()  # Breakpoint to inspect request data 
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

#Getters
def get_users(request): #users
    try: 
        users = list(User.objects.values('id', 'username', 
'email', 'created_at')) 
        return JsonResponse(users, safe=False) 
    except Exception as e: 
        return JsonResponse({'error': str(e)}, status=500)

def get_posts(request): #posts
    try: 
        posts = list(Post.objects.values('id', 'content', 
'author', 'created_at')) 
        return JsonResponse(posts, safe=False) 
    except Exception as e: 
        return JsonResponse({'error': str(e)}, status=500)