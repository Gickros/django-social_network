from typing import Any

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.text import slugify

User = get_user_model()


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PUBLISHED = "published", "Опубликовано"

    title = models.CharField(max_length=100)
    desc = models.CharField(verbose_name="description", max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/")
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


class Like(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post", "author"],
                condition=Q(is_active=True),
                name="unique_post_author",
            )
        ]


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow",
            )
        ]