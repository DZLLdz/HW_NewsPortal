from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .filters import PostFilter
from .forms import PostForm


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        if '/articles/create' in self.request.path:
            post.post_type = 'ART'
        if '/news/create' in self.request.path:
            post.post_type = 'NEWS'
        return super().form_valid(form)


class PostsList(ListView):
    model = Post
    ordering = '-post_add'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        context['filterset'] = self.filterset
        return context


class ArtsList(ListView):
    model = Post
    ordering = '-post_add'
    template_name = 'articles.html'
    context_object_name = 'arts'
    paginate_by = 10
    queryset = Post.objects.filter(post_type=Post.article_post)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        return context


class ArtsSearchList(ListView):
    model = Post
    ordering = '-post_add'
    template_name = 'articles_search.html'
    context_object_name = 'arts_search'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.filter(post_type=Post.article_post)
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        context['filterset'] = self.filterset
        return context


class ArtDetail(DetailView):
    model = Post
    template_name = 'art_detail.html'
    context_object_name = 'art'
    queryset = Post.objects.filter(post_type=Post.article_post)


class ArtUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'art_update.html'
    queryset = Post.objects.filter(post_type=Post.article_post)


class ArtDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'art_delete.html'
    queryset = Post.objects.filter(post_type=Post.article_post)
    success_url = reverse_lazy('arts_list')


class NewsList(ListView):
    model = Post
    ordering = '-post_add'
    template_name = 'news.html'
    context_object_name = 'newss'
    paginate_by = 10
    queryset = Post.objects.filter(post_type=Post.news_post)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        return context


class NewsSearchList(ListView):
    model = Post
    ordering = '-post_add'
    template_name = 'articles_search.html'
    context_object_name = 'news_search'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.filter(post_type=Post.article_post)
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news'
    queryset = Post.objects.filter(post_type=Post.news_post)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_update.html'
    queryset = Post.objects.filter(post_type=Post.news_post)
    success_url = reverse_lazy('news_list')


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    queryset = Post.objects.filter(post_type=Post.news_post)
    success_url = reverse_lazy('news_list')
