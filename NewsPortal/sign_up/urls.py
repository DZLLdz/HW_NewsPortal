import django.contrib.auth.views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, out, upgrade_to_author

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('logout/',
         out,),
    path('signup/',
         BaseRegisterView.as_view(template_name='sign/signup.html'),
         name='signup'),
    path('upgrade/', upgrade_to_author, name='upgrade')
]
