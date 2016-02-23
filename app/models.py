from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from imagekit.models import ImageSpecField


class Picture(models.Model):
    """Model holding picture data and fields. """
    image = ProcessedImageField([ResizeToFit(1920, 1200, False)])
    thumbnail = ImageSpecField(
        source='image', processors=[ResizeToFit(300, 150)],
        format='JPEG')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']


class EffectType(models.Model):
    """Model holding effect and filter types. """
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{0}'.format(self.name)


class Effect(models.Model):
    """Model holding effects and filters. """
    name = models.CharField(max_length=50)
    effect_type = models.ForeignKey(EffectType, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{0}'.format(self.name)


class Edits(models.Model):
    """Model holding edited images data. """
    image_name = models.ImageField('img', upload_to='edits/')
    effect = models.CharField(max_length=50)
    parent_pic = models.ForeignKey(Picture, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
