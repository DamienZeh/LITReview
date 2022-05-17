from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from . import models
User = get_user_model()


class FluxForm(forms.Form):
    pass


class ImageForm(forms.ModelForm):
    class Meta:
        model = models.Image
        fields = ['image']


class TicketForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                           'placeholder': 'Titre du livre + auteur'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control',
                           'placeholder': 'Pas obligatoire pour une demande.'}))
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description']


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
