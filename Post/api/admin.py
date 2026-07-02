from django.contrib import admin

from .models import Comment, Follow, Like, Post, Profile


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (CommentInline, LikeInline)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "created_at")
    search_fields = ("author__username", "post__title")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "is_active", "created_at")
    list_filter = ("is_active",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "bio")
    search_fields = ("user__username",)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "follower", "following", "created_at")
    search_fields = ("follower__username", "following__username")