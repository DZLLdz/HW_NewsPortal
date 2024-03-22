from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.generic.edit import CreateView

from .models import BaseRegisterForm


def out(request):
    logout(request)
    return TemplateResponse(request, 'sign/login.html')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_to_author(request):
    user = request.user
    author_group = Group.objects.get(name='writer')
    if not request.user.groups.filter(name='writer').exists():
        author_group.user_set.add(user)
    return redirect('/')
