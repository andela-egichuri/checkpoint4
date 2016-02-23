import os
import shutil
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.core import serializers
from PIL import Image
from .effects import EditImage
from .models import Picture, Effect, Edits
from .forms import ImageUploadForm


def index(request):
    """ Application landing page. """
    if request.user.is_authenticated() and request.user.is_active:
        return HttpResponseRedirect('/dashboard')
    content = {}
    return render(request, 'index.html', content)


@login_required
def dashboard(request):
    """Application dashboard.

    Displays images and effects. Also handles file upload
    """
    content = {}
    content['new_files'] = []
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            for afile in request.FILES.getlist('image'):
                newimage = Picture(image=afile)
                newimage.owner = request.user
                newimage.save()
                content['new_files'].append(newimage.pk)
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
    """Method to handle image manipulation.

    Calls the appropriate methods from the EditImage class
    """
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

    url = 'temp/' + edited
    data = {'url': url}
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@require_http_methods(["GET", "POST"])
def get_image(request):
    """Return image data when passed the image ID. """

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
    """Perform image delete.

    Deletes both the image and its data. Including effects generated.
    """
    data = {}
    id = request.POST['id']
    try:
        pic = Picture.objects.get(id=id)
        thumb = pic.thumbnail.path
        pic_path = pic.image.path
        pic_name = os.path.basename(pic.image.name)
        temp_path = os.path.dirname(pic_path) + \
            '/temp/' + os.path.splitext(pic_name)[0]

        edits = Edits.objects.filter(parent_pic=pic)
        for item in edits:
            item_path = os.path.dirname(pic_path) + item.image_name.url
            if os.path.exists(item_path):
                os.remove(item_path)

        if os.path.exists(os.path.dirname(thumb)):
            shutil.rmtree(os.path.dirname(thumb))
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        if os.path.exists(pic_path):
            os.remove(pic_path)
        pic.delete()
        data['status'] = 'delete complete'
    except Exception:
        data['status'] = 'error'

    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
@require_http_methods(["POST"])
def save(request):
    """Save an image given its name and effect applied. """
    pic_name = request.POST['name']
    pic_parent = Picture.objects.get(id=request.POST['original'])
    effect = request.POST['effect']
    if effect == '':
        effect = 'None'
    pic = os.path.join(settings.BASE_DIR, 'public' + pic_name)
    dir_name = settings.MEDIA_ROOT + "/edits/" + effect + "/"
    if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    par_name = pic_parent.image.name
    pic_path = pic_parent.image.path
    dest = dir_name + os.path.basename(par_name)
    temp_path = os.path.dirname(pic_path) + \
        '/temp/' + os.path.splitext(par_name)[0]
    try:
        shutil.copy(pic, dest)
        edited = Edits()
        image_name = "/edits/" + effect + "/" + os.path.basename(dest)
        Edits.objects.update_or_create(
            image_name=image_name, effect=effect, parent_pic=pic_parent)
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
    except Exception:
        raise

    data = {'pic_name': dest, 'effect': effect}
    return HttpResponse(json.dumps(data), content_type="application/json")


def sizeof_fmt(num, suffix='B'):
    """Change file size format. """
    for unit in [' ', ' K', ' M', ' G', ' T', ' Pi', ' Ei', ' Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
