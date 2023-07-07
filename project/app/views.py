from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .forms import NameForm

def index(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            old_name = request.session.get('name')
            if old_name is not None and old_name != name:
                messages.success(request, 'Looks like you have changed your name!')
            request.session['name'] = name
            return HttpResponseRedirect(reverse('app:index'))
    form = NameForm()
    context = {
        'current_time': timezone.now(), 
        'form': form, 
        'name': request.session.get('name'),
    }
    return render(request, 'app/index.html', context)

def user(request, name):
    context = {'name': name}
    return render(request, 'app/user.html', context)
