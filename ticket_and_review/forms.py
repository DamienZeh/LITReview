from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from . import models
User = get_user_model()

class FluxForm(forms.Form):
    pass



class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image']


class BlogForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                           'placeholder': 'Titre du livre + auteur'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control',
                           'placeholder': 'Pas obligatoire pour une demande.'}))
    edit_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Blog
        fields = ['title', 'description']



class DeleteBlogForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)
