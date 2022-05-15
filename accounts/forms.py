from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignupForm(UserCreationForm):

    username = forms.CharField(max_length=63,
                               widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur"}),
                               label='Nom d’utilisateur', error_messages={'unique': 'Cet utilisateur existe déjà !'})
    password1 = forms.CharField(max_length=63,
                                widget=forms.PasswordInput
    (attrs={'placeholder': "Mot de passe"}),
                                label='Mot de passe')
    password2 = forms.CharField(max_length=63,
                                widget=forms.PasswordInput
    (attrs={'placeholder': "Confirmer mot de passe"}),
                                label='Mot de passe')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63,
                               widget= forms.TextInput
    (attrs={'placeholder': "Nom d'utilisateur"}),
                               label='Nom d’utilisateur')
    password = forms.CharField(max_length=63,
                               widget=forms.PasswordInput
    (attrs={'placeholder': "Mot de passe"}),
                               label='Mot de passe')