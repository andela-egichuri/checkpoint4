from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from imagekit.models import ImageSpecField


class Image(models.Model):
    image = ProcessedImageField([ResizeToFit(1920, 1200, False)])
    thumbnail = ImageSpecField(
        source='image', processors=[ResizeToFit(300, 150)],
        format='JPEG')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
