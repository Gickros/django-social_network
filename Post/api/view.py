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


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    queryset = Post.objects.annotate(
        comments_count=Count('comments'),
        likes_count=Count('likes'),filter=Q(likes__is_active=True)
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
    @action(detail=False,methods=['post'])
    def toggle(self,request,pk=None):
        user = request.user
        post_id = request.data.get('post_id')

        post = get_object_or_404(Post, pk=post_id)

        like = Like.objects.filter(post=post, author=user).first()
        if like:
            like.is_active =not like.is_active
            like.save()
            
        else:   
            like=Like.objects.create(post=post,author=user,is_active=True)
        serializer = self.get_serializer(like)
        return Response(serializer.data)