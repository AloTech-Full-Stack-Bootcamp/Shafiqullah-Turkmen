### Task 1: Serializers / HyperlinkedModelSerializer / ModelSerializer
### Solution:
#### serializers.py
```python
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
```

### Task 2: Authentication / JWT / - drf-yasg, Swagger
### Solution: 
### urls.py
```python
from django.contrib import admin
from django.urls import path,include, re_path
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from main.views import UserViewSet, PostViewSet, CommentViewSet, LikeViewSet

# registers ViewSets to routers.DefaultRouter(), routers by django_rest_framework :D
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)

# For Swagger UI
schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

### Task 3: Permissions / Aciton
### Solution: 
### views.py
```python
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
    
    # Solution to Like problem
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

```
