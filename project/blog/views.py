from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import LoginForm, RegistrationForm

def index(request):
    return render(request, 'blog/index.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            u = User.objects.get(email=email)
            if not u:
                messages.warning(request, 'Invalid email.')
                return HttpResponseRedirect(reverse('blog:login'))
            user = authenticate(request, username=u.username, password=password)
            if user is not None:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(settings.KEEP_LOGGED_DURATION)
                next = request.GET.get('next')
                if next is None or not next.startswith('/'):
                    next = HttpResponseRedirect(reverse('blog:index'))
                else:
                    next = redirect(next)
                return next
            else:
                messages.warning(request, 'Invalid username or password.')
                return HttpResponseRedirect(reverse('blog:login'))
    form = LoginForm()
    context = {'form': form}
    return render(request, 'blog/login.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return HttpResponseRedirect(reverse('blog:index'))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User(email=email, username=username, password=password)
            user.save()
            messages.success(request, 'You can now login.')
            return HttpResponseRedirect(reverse('blog:login'))
    form = RegistrationForm()
    context = {'form': form}
    return render(request, 'blog/register.html', context)

@login_required
def secret(request):
    return HttpResponse('Only authenticated users are allowed!')

def user(request, name):
    context = {'name': name}
    return render(request, 'blog/user.html', context)
