from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Post, Comment


class PostsList(ListView):
    model = Post
    ordering = '-post_name'
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        return context
class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'