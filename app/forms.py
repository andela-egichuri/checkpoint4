from django import forms
from models import Image


class ImageUploadForm(forms.ModelForm):
    """Image upload form."""

    class Meta:
        model = Image
        exclude = ('thumbnail', 'owner',)
        widgets = {'image': forms.FileInput(
            attrs={
                'class': 'form-control', 'required': True,
                'multiple': 'multiple'
            }
        )}