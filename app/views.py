from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from models import Image
from forms import ImageUploadForm


def index(request):
    """Application Dashboard. """
    if request.user.is_authenticated() and request.user.is_active:
        return HttpResponseRedirect('/dashboard')
    content = {}
    return render(request, 'index.html', content)


# @login_required
def dashboard(request):
    """Application dashboard. """
    content = {}
    # Handle file upload
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            newimage = Image(image=request.FILES['image'])
            newimage.owner = request.user
            newimage.save()
            return HttpResponseRedirect('/dashboard')
    else:
        form = ImageUploadForm()
    images = Image.objects.filter(owner=request.user)

    content['images'] = images
    content['form'] = form
    return render(request, 'dashboard.html', content)
