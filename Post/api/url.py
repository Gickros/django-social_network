from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CommentViewSet,
    FollowViewSet,
    LikeViewSet,
    PostViewSet,
    ProfileViewSet,
    RegisterApiView,
)

router = DefaultRouter()

router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"profiles", ProfileViewSet, basename="profile")
router.register(r"follows", FollowViewSet, basename="follow")
router.register(r"likes", LikeViewSet, basename="like")

urlpatterns = [
    path("auth/register/", RegisterApiView.as_view(), name="register"),
] + router.urls