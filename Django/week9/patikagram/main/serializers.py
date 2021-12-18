from rest_framework import serializers
from django.contrib.auth.models import User
from . models import Comment, Like, Post

# Serializer for User api
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

# Serializer for Post api
class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    likes_count_comments_count = serializers.SerializerMethodField()


    class Meta:
        model = Post
        fields = ['id', 'author', 'created_at', 'image', 'content', 'likes_count', 'comments_count', 'likes_count_comments_count']

    
    def get_likes_count_comments_count(self, object):
        return f"Likes: {object.likes_count} / Comments: {object.comments_count}"

# Serializer for Comment api
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at']

# Serializer for Like api
class LikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']