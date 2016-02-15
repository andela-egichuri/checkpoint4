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
            # Redirect to the document list after POST
            return HttpResponseRedirect('/dashboard')
    else:
        form = ImageUploadForm()
    # Load documents for the list page
    # import ipdb; ipdb.set_trace()
    images = Image.objects.filter(owner=request.user)
    # import ipdb; ipdb.set_trace()

    content['images'] = images
    content['form'] = form
    return render(request, 'dashboard.html', content)


# def list(request):
#     image_content = {}
#     # Handle file upload
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             newimage = Image(image=request.FILES['image'])
#             newimage.save()

#             # Redirect to the document list after POST
#             return HttpResponseRedirect(reverse('myapp.views.list'))
#     else:
#         form = ImageUploadForm()

#     # Load documents for the list page
#     images = Image.objects.all()

#     image_content = {'images': images, 'form': form},
#     import ipdb; ipdb.set_trace()
#     # Render list page with the documents and the form
#     return render(request, 'dashboard.html', image_content)