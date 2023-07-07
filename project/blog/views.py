from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import NameForm

def index(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            user = User.objects.filter(username=name).first()
            if not user:
                user = User(username=name)
                user.save()
                request.session['known'] = False
            else:
                request.session['known'] = True
            request.session['name'] = name
            return HttpResponseRedirect(reverse('blog:index'))
    form = NameForm()
    context = {
        'current_time': timezone.now(), 
        'form': form, 
        'name': request.session.get('name'),
        'known': request.session.get('known', False),
    }
    return render(request, 'blog/index.html', context)

def user(request, name):
    context = {'name': name}
    return render(request, 'blog/user.html', context)
