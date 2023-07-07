from django.shortcuts import render
from django.utils import timezone

def index(request):
    context = {'current_time': timezone.now()}
    return render(request, 'app/index.html', context)

def user(request, name):
    context = {'name': name}
    return render(request, 'app/user.html', context)
