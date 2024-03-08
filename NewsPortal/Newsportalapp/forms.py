from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Category, Author


class PostForm(forms.ModelForm):
    # categories = forms.ModelMultipleChoiceField(
    #     queryset=Category.objects.all(),
    #     label='Add category',
    # )
    #
    # post_author = forms.ModelChoiceField(
    #     queryset=Author.objects.all(),
    #     label='Укажите авторство',
    # )
    class Meta:
        model = Post
        fields = [
            'post_name',
            'post_text',
            'post_author',
            'categories',
        ]

    def clean(self):
        cleaned_data = super().clean()
        post_text = cleaned_data.get('post_text')
        post_name = cleaned_data.get('post_name')
        if post_text is not None and len(post_text) < 20:
            raise ValidationError({
                'post_text': 'Пост не может содержать менее 20 символов'
            })
        if post_text == post_name:
            raise ValidationError({
                'post_name': 'Название поста должно быть отличительным от содержания'
            })

        return cleaned_data
