import os
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings

from PIL import Image, ImageFilter, ImageOps


class EditImage(object):

    def __init__(self, image):
        self.temp_dir = os.path.splitext(image)[0]
        self.temp_dir = os.path.dirname(image) + '/edited/'
        self.filename = os.path.basename(image)
        self.image = Image.open(image)

    def rotate(self, angle):
        tempfile = self.temp_dir + "rotate." + self.filename
        to_save = self.image.rotate(angle)
        to_save.save(tempfile)
        return tempfile

    def flip(self, direction):
        pass

    def detail(self, direction):
        pass

    def contrast(self, direction):
        pass

    def smooth(self, direction):
        pass

    def emboss(self, direction):
        pass

    def flip(self, direction):
        pass

    def sharpen(self, direction):
        pass

    def grayscale(self, direction):
        pass
