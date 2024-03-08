from django import forms
from django_filters import FilterSet, ModelChoiceFilter, DateFilter

from .models import Post, Category


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='ALL',
    )

    post_add = DateFilter(widget=forms.DateInput(attrs={'type': 'date'}),
                          label='Date add greater then',
                          lookup_expr='date__gte',)

    class Meta:
        model = Post
        fields = {
            'post_name': ['icontains'],
            'post_author__name_author__username': ['icontains'],
        }
