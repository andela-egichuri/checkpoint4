from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


def index(request):
    """Application Dashboard"""
    if request.user.is_authenticated() and request.user.is_active:
        return HttpResponseRedirect('/dashboard')

    content = {}
    return render(request, 'index.html', content)


@login_required
def dashboard(request):
    """Application dashboard"""
    return render(request, 'dashboard.html', {})
