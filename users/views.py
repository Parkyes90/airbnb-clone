import json
import os

import requests
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView

from users import forms
from users.models import User


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "ye",
        "last_name": "park",
        "email": "test@test123.com",
        "password": "12",
        "password1": "12",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # TODO: add success Message
    except User.DoesNotExist:
        # TODO: add error Message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://localhost:8111/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        if code is not None:
            res = requests.post(
                f"https://github.com/login/oauth/access_token"
                f"?client_id={client_id}"
                f"&client_secret={client_secret}"
                f"&code={code}",
                headers={"Accept": "application/json"},
            )
            res_json = res.json()
            error = res_json.get("error", None)
            if error is not None:
                raise GithubException()
            else:
                access_token = res_json.get("access_token")
                api_res = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = api_res.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    if email is None:
                        raise GithubException()
                    try:
                        user = User.objects.get(email=email)
                        if user.login_method != User.LOGIN_GITHUB:
                            raise GithubException()
                    except User.DoesNotExist:
                        user = User.objects.create(
                            username=email,
                            first_name=name,
                            bio=bio,
                            email=email,
                            login_method=User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()

                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        raise GithubException()

    except GithubException:
        return redirect(reverse("users:login"))
