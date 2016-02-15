from django.contrib import admin
from .models import Image
# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'image', 'owner'
    )

admin.site.register(Image, ImageAdmin)