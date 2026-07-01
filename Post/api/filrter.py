import django_filters
from .models import Post


class Postfilter(django_filters.FilterSet):
    author=django_filters.CharFilter(field_name='author',lookup_expr='icontaints')
    created_after = django_filters.DateTimeFilter(field_name='created_at',lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at',lookup_expr = 'lte')
    class Meta:
        model= Post
        field = ['created_at','author']