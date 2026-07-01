from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    CommentViewSet,
    ProfileViewSet,
    FollowViewSet,
    LikeViewSet,
)


router = DefaultRouter()

router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"profiles", ProfileViewSet)
router.register(r"follows", FollowViewSet)
router.register(r"likes", LikeViewSet)

urlpatterns = router.urls
