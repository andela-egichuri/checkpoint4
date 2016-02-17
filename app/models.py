from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from imagekit.models import ImageSpecField


class Picture(models.Model):
    image = ProcessedImageField([ResizeToFit(1920, 1200, False)])
    thumbnail = ImageSpecField(
        source='image', processors=[ResizeToFit(300, 150)],
        format='JPEG')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']


class EffectType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{0}'.format(self.name)


class Effect(models.Model):
    name = models.CharField(max_length=50)
    effect_type = models.ForeignKey(EffectType, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{0}'.format(self.name)