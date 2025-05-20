import django_filters
from .models import Post, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title contains:')
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = []