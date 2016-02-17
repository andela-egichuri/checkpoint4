import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from PIL import Image
from effects import EditImage
from models import Picture
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
            newimage = Picture(image=request.FILES['image'])
            newimage.owner = request.user
            newimage.save()
            return HttpResponseRedirect('/dashboard')
    else:
        form = ImageUploadForm()
    images = Picture.objects.filter(owner=request.user)
    content['images'] = images
    content['form'] = form
    return render(request, 'dashboard.html', content)


@require_http_methods(["GET", "POST"])
def edit(request):
    # import ipdb; ipdb.set_trace()
    id = request.POST['id']
    effect = request.POST['effect']
    pic = Picture.objects.get(id=id)
    pic_path = pic.image.path
    url = EditImage(pic_path).rotate(45)
    data = {'url': url}
    return JsonResponse(data)


def getmethod(*args):
    id_to_method = {
        'rotate': rotate,
        'smooth': smooth
    }

    return id_to_method