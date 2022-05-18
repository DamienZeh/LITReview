from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from . import models



class FluxForm(forms.Form):
    pass


class TicketForm(forms.ModelForm):
    title = forms.CharField(label='Titre', widget=forms.Textarea(attrs={'class': 'form-control',
                           'placeholder': 'Titre du livre + auteur', 'cols': 60, 'rows': 1}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control',
                           'placeholder': 'Pas obligatoire pour une demande.', 'cols': 60 }))
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    image = forms.ImageField(label='', error_messages={'invalid': "Image files only"},
                             widget=forms.FileInput(attrs={'class': 'django_btn'}))

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
