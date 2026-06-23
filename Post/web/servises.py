from django.shortcuts import get_object_or_404
from .models import Post


def get_post(post_pk):
    return get_object_or_404(Post, pk=post_pk)