import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.core import serializers
from PIL import Image
from effects import EditImage
from models import Picture, Effect
from forms import ImageUploadForm


def index(request):
    """Application Dashboard. """
    if request.user.is_authenticated() and request.user.is_active:
        return HttpResponseRedirect('/dashboard')
    content = {}
    return render(request, 'index.html', content)


@login_required
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
    effects = Effect.objects.all()
    content['images'] = images
    content['effects'] = effects
    content['form'] = form
    return render(request, 'dashboard.html', content)


@login_required
@require_http_methods(["POST"])
def edit(request):
    id = request.POST['id']
    effect_name = request.POST['effect']
    if effect_name == 'enhance':
        enhancement = {}
        enhancement['color'] = float(request.POST['color'])
        enhancement['contrast'] = float(request.POST['contrast'])
        enhancement['sharpness'] = float(request.POST['sharpness'])
        enhancement['brightness'] = float(request.POST['brightness'])

    pic = Picture.objects.get(id=id)
    pic_path = pic.image.path

    effect = Effect.objects.filter(name=effect_name)
    to_apply = EditImage(pic_path, effect_name)
    effect_type = effect[0].effect_type.name

    if effect_type == 'image':
        edited = to_apply.basic_effects()

    elif effect_type == 'imageenhance':
        edited = to_apply.enhancements(enhancement)

    elif effect_type == 'imagefilter':
        edited = to_apply.filters()

    elif effect_type == 'imageops':
        edited = to_apply.operations()

    url = 'media/edited/' + edited
    data = {'url': url}
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_method(*args):
    id_to_method = {
        'rotate': rotate,
        'smooth': smooth
    }

    return id_to_method


@login_required
@require_http_methods(["POST"])
def get_image(request):
    image = {}
    id = request.POST['id']
    pic = Picture.objects.get(id=id)
    import ipdb; ipdb.set_trace()
    image['pic_name'] = pic.image.name
    image['pic_id'] = pic.id
    image['thumbnail'] = pic.thumbnail.url
    image['pic_path'] = pic.image.path
    image['url'] = pic.image.url
    return HttpResponse(json.dumps(image), content_type="application/json")
