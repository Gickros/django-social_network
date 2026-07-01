from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404

from .models import Post, Profile, Comment, Follow, Like
from .serializers import (
    PostSerializer,
    ProfileSerializer,
    CommentSerializer,
    FollowSerializer,
    LikeSerializer
)
from .services import toggle_like
from .filter.py import Post.filter


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_classes = PostFilter
    filter_backends = [
    DjangoFilterBackend,
    SearchFilter,
    OrderingFilter
]

    search_fields = ['created_at','author']

    queryset = Post.objects.annotate(
        comment_count=Count('comments'),
        likes_count=Count('likes', filter=Q(likes__is_active=True))
    )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


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
        user = request.user
        post_id = request.data.get("post_id")

        post = get_object_or_404(Post, id=post_id)

        like = toggle_like(user=user, post=post)

        return Response({
            "is_active": like.is_active
        })