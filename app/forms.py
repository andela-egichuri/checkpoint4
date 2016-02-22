from django import forms
from .models import Picture


class ImageUploadForm(forms.ModelForm):
    """Image upload form."""

    class Meta:
        model = Picture
        exclude = ('thumbnail', 'owner',)
        widgets = {'image': forms.FileInput(
            attrs={
                'class': 'form-control', 'required': True,
                'multiple': 'multiple'
            }
        )}