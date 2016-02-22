import os
import shutil

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
        # import ipdb; ipdb.set_trace()
        if form.is_valid():
            for afile in request.FILES.getlist('image'):
                newimage = Picture(image=afile)
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
    image['pic_name'] = os.path.basename(pic.image.name)
    image['pic_id'] = pic.id
    image['thumbnail'] = pic.thumbnail.url
    image['pic_path'] = pic.image.path
    image['url'] = pic.image.url
    image['added'] = "{:%d %b %Y}".format(pic.date_created)
    image['size'] = sizeof_fmt(pic.image.size)
    image['width'] = pic.image.width
    image['height'] = pic.image.height
    return HttpResponse(json.dumps(image), content_type="application/json")


@login_required
@require_http_methods(["POST"])
def delete(request):
    data = {}
    id = request.POST['id']
    try:
        pic = Picture.objects.get(id=id)
        thumb = pic.thumbnail.path
        pic_path = pic.image.path
        pic_name = os.path.basename(pic.image.name)
        edits_path = os.path.dirname(pic_path) + '/edited/' + os.path.splitext(pic_name)[0]

        if os.path.exists(os.path.dirname(thumb)):
            shutil.rmtree(os.path.dirname(thumb))
        if os.path.exists(edits_path):
            shutil.rmtree(edits_path)
        if os.path.exists(pic_path):
            os.remove(pic_path)
        pic.delete()
        data['status'] = 'complete'
    except:
        data['status'] = 'error'

    return HttpResponse(json.dumps(data), content_type="application/json")


def sizeof_fmt(num, suffix='B'):
    for unit in [' ', ' K', ' M', ' G', ' T', ' Pi', ' Ei', ' Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)