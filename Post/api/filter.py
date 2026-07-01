import django_filters

from .models import Post


class PostFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(
        field_name="author__username", lookup_expr="icontains"
    )
    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    class Meta:
        model = Post
        fields = ["status", "author"]