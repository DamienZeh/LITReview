from django import forms
from django.contrib.auth import get_user_model
from .models import UserFollows, Ticket, Review

User = get_user_model()


class TicketForm(forms.ModelForm):
    """
    Form for ticket
    """

    title = forms.CharField(
        label="Titre",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Titre du livre + auteur",
                "cols": 60,
                "rows": 1,
            }
        ),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Pas obligatoire pour une demande.",
                "cols": 60,
            }
        ),
    )
    image = forms.ImageField(
        label="",
        required=False,
        error_messages={"invalid": "Image files only"},
        widget=forms.FileInput(attrs={"class": "django_btn"}),
    )

    class Meta:
        """
        Meta for Ticket. Fields : 'title', 'description', 'image'
        """

        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    """
    Form for review
    """

    headline = forms.CharField(
        label="Titre",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Titre de la critique",
                "cols": 60,
                "rows": 1,
            }
        ),
    )
    body = forms.CharField(
        label="Description",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Commentaire de la critique.",
                "cols": 60,
            }
        ),
    )

    number_rating = (
        ("0", " - 0"),
        ("1", " - 1"),
        ("2", " - 2"),
        ("3", " - 3"),
        ("4", " - 4"),
        ("5", " - 5"),
    )
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=number_rating)

    class Meta:
        """
        Meta for Review. Fields : 'image', 'headline', 'rating', 'body'
        """

        model = Review
        fields = ["headline", "rating", "body"]


class DeletePostForm(forms.Form):
    delete_post = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class FollowUsersForm(forms.ModelForm):
    """
    form for follow users
    """

    class Meta:
        """
        Meta for FollowUserForm. Fields : 'followed_user'
        """

        model = UserFollows
        fields = ["followed_user"]
