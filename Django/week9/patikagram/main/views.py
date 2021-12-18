from django.db.models import query
from rest_framework import viewsets
from django.contrib.auth.models import User
from . models import Comment, Like, Post
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response

from main.serializers import PostSerializer, UserSerializer, CommentSerializer, LikeSerializer

# ViewSet for User model
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# ViewSet for Post model
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    # Solution for Like problem
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        query_set_object = Like.objects.get_or_create(post=post, user=user)
        if len(query_set_object) == 0:   
            query_set_object.create(post=post, user=user)
            return Response(data={'msg': 'liked'})
        else: 
            query_set_object.delete()
            return Response(data={'msg': 'unliked'})
            


# ViewSet for Comment model
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer 
    permission_classes = [IsAuthenticated]

    
# ViewSet for Like model
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer 
    permission_classes = [IsAuthenticated]
