from django.db import models

# Create your models here. 
class User(models.Model): 
    username = models.CharField(max_length=100, unique=True)  # User's unique username 
    email = models.EmailField(unique=True)  # User's unique email 
    created_at = models.DateTimeField(auto_now_add=True)  #Timestamp when the user was created 
    def __str__(self): 
        return self.username 

class Post(models.Model): 
    content = models.TextField()  # The text content of the post 
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who created the post 
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post was created 
    def __str__(self): 
        return self.content[:50]

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]
