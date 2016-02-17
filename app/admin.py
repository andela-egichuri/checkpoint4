from django.contrib import admin
from .models import Picture
# Register your models here.


class PicAdmin(admin.ModelAdmin):
    list_display = (
        'image', 'owner'
    )

admin.site.register(Picture, PicAdmin)