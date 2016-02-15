from django import forms
from models import Image


class ImageUploadForm(forms.ModelForm):
    """Image upload form."""
    # image = forms.ImageField(widget=forms.FileInput(
    #     attrs={'class': 'form-control', 'required': True})
    # )
    class Meta:
        model = Image
        exclude = ('thumbnail', 'owner',)
        widgets = {'image': forms.FileInput(
            attrs={'class': 'form-control', 'required': True})
        }