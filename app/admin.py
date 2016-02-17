from django.contrib import admin
from .models import Picture, Effect, EffectType
# Register your models here.


class PicAdmin(admin.ModelAdmin):
    list_display = (
        'image', 'owner'
    )


class EffectsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'effect_type', 'status'
    )


class EffectTypesAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

admin.site.register(Picture, PicAdmin)
admin.site.register(Effect, EffectsAdmin)
admin.site.register(EffectType, EffectTypesAdmin)
