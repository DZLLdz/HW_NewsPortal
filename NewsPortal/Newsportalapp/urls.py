from django.urls import path
from .views import (NewsList, NewsSearchList, NewsDetail, NewsUpdate, NewsDelete,
                    ArtsList, ArtsSearchList, ArtDetail, ArtUpdate, ArtDelete,
                    PostsList, PostCreate,)


urlpatterns = [
    path('all_posts/', PostsList.as_view(), name='post_list'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/search', NewsSearchList.as_view(), name='news_search'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/', ArtsList.as_view(), name='arts_list'),
    path('articles/create/', PostCreate.as_view(), name='post_create'),
    path('articles/search', ArtsSearchList.as_view(), name='arts_search'),
    path('articles/<int:pk>/', ArtDetail.as_view(), name='art_detail'),
    path('articles/<int:pk>/update/', ArtUpdate.as_view(), name='art_update'),
    path('articles/<int:pk>/delete/', ArtDelete.as_view(), name='art_delete'),
]
