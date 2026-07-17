from django.db.models import Count, Q
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from .filter import PostFilter
from .models import Comment, Follow, Like, Post, Profile
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    LikeSerializer,
    PostSerializer,
    ProfileSerializer,
    RegisterSerializer,
)
from .services import toggle_like


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Post.objects.annotate(
        comment_count=Count("comments"),
        likes_count=Count("likes", filter=Q(likes__is_active=True)),
    )

    filterset_class = PostFilter
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = ["title", "desc", "author__username",]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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

    queryset = Profile.objects.select_related("user").annotate(
        followers_count=Count("user__followers"),
        following_count=Count("user__following"),
    )


class LikeViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def toggle(self, request):
        post = get_object_or_404(Post, id=request.data.get("post_id"))

        like = toggle_like(
            user=request.user,
            post=post,
        )

        return Response(
            {
                "is_active": like.is_active,
            }
        )


class RegisterApiView(generics.CreateAPIView):
    serializer_class = RegisterSerializer