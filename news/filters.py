import django_filters
from django_filters import DateTimeFilter
from django.forms import DateTimeInput
from .models import News


class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label="Заголовок"
    )

    category = django_filters.CharFilter(
        field_name='category__name',
        lookup_expr='icontains',
        label="Категория"
    )

    date_after = DateTimeFilter(
        field_name='published_at',
        lookup_expr='gt',
        widget=DateTimeInput(
            attrs={'type': 'datetime-local'}
        ),
        label="Дата после"
    )

    class Meta:
        model = News
        fields = ['title', 'category', 'date_after']
