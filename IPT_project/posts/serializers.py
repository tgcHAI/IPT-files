from rest_framework import serializers
from .models import User, Post, Comment
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'created_at']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField to allow passing IDs for author and post
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Comment text cannot be empty.")
        return value

class PostSerializer(serializers.ModelSerializer):
    # Include nested comments in the post serializer
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'comments']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Post content cannot be empty.")
        return value
