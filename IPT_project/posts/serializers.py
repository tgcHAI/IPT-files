from rest_framework import serializers
from .models import User, Post
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'created_at']

    def create(self, validated_data):
        # Encrypt the password before saving the user
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at']
