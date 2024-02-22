from django.contrib import admin
from django.urls import path, include

from Newsportalapp.views import PostsList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('Newsportalapp.urls'))
]
