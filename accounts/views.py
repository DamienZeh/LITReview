from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from . import forms


def logout_user(request):
    """
    logout user and redirect to login page
    """
    logout(request)
    return redirect("login")


def login_page(request):
    """
    user can logins thanks to LoginForm.
    """
    form = forms.LoginForm()
    message = ""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("flux")
            else:
                message = "Identifiants invalides."
    return render(
        request,
        "accounts/login.html",
        context={"form": form, "message": message},
    )


def signup_page(request):
    """
    allows to create an account. Then goes to the flux page.
    """
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "accounts/signup.html", context={"form": form})
