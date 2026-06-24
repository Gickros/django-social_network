from rest_framework import viewsets
from django.db.models import Count
from .models import Post, Profile, Comment, Follow, Like
from .serializers import (
    PostSerializer,
    ProfileSerializer,
    CommentSerializer,
    FollowSerializer,
    LikeSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .services import toogle_like
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

      queryset = Post.objects.annotate(
        comment_count=Count('comments'),
        likes_count=Count('likes', filter=Q(likes__is_active=True))
    )

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()




class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer

    queryset = Profile.objects.select_related('user').annotate(
        followers_count=Count('user__followers'),
        following_count=Count('user__following')
    )


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
  @action(detail=False, methods=['post'])
def toggle(self, request):
 like=toogle_like(user,post)