import os

import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib import messages

from users import forms
from users.mixins import (
    LoggedOutOnlyView,
    LoggedInOnlyView,
    EmailLoginOnlyView,
)
from users.models import User


class LoginView(LoggedOutOnlyView, FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user:
            messages.success(self.request, f"Welcome back! {user.first_name}")
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg

        return reverse("core:home")


def log_out(request):
    messages.info(request, f"See you later {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(LoggedOutOnlyView, FormView):
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

        if code is None:
            raise GithubException("Something went wrong.")

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
            raise GithubException("Something went wrong.")
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
        if username is None:
            raise GithubException("Something went wrong.")

        name = profile_json.get("name")
        email = profile_json.get("email")
        bio = profile_json.get("bio")
        avatar_url = profile_json.get("avatar_url")
        if email is None:
            raise GithubException("Please also give me your email.")
        try:
            user = User.objects.get(email=email)
            if user.login_method != User.LOGIN_GITHUB:
                raise GithubException(
                    f"Please Log in with: {user.login_method}"
                )
        except User.DoesNotExist:
            user = User.objects.create(
                username=email,
                first_name=name,
                bio=bio,
                email=email,
                login_method=User.LOGIN_GITHUB,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if avatar_url is not None:
                photo_request = requests.get(avatar_url)
                user.avatar.save(
                    f"{name}-avatar", ContentFile(photo_request.content)
                )
        messages.success(request, f"Welcome back! {user.first_name}")
        login(request, user)
        return redirect(reverse("core:home"))
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("K_KEY")
    redirect_uri = "http://localhost:8111/users/login/kakao/callback"
    return redirect(
        f"https:/kauth.kakao.com/oauth/authorize"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
    )


class KaKaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("K_KEY")
        redirect_uri = "http://localhost:8111/users/login/kakao/callback"
        if code is None:
            raise KaKaoException("Something went wrong")
        res = requests.post(
            f"https://kauth.kakao.com/oauth/token"
            f"?client_id={client_id}"
            f"&code={code}"
            f"&grant_type=authorization_code"
            f"&redirect_uri={redirect_uri}",
            headers={"Accept": "application/json"},
        )
        res_json = res.json()
        error = res_json.get("error", None)
        if error is not None:
            raise KaKaoException("Can't get authorization code.")
        access_token = res_json.get("access_token")
        api_res = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )
        profile_json = api_res.json()
        kakao_account = profile_json.get("kakao_account", {})
        email = kakao_account.get("email")
        if email is None:
            raise KaKaoException("Please also give me your email.")

        profile = kakao_account.get("profile", {})
        nickname = profile.get("nickname")
        profile_image = profile.get("thumbnail_image_url")
        try:
            user = User.objects.get(email=email)
            if user.login_method != User.LOGIN_KAKAO:
                raise KaKaoException(
                    f"Please Log in with: {user.login_method}"
                )
        except User.DoesNotExist:
            user = User.objects.create(
                username=email,
                first_name=nickname,
                email=email,
                login_method=User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        messages.success(request, f"Welcome back! {user.first_name}")
        login(request, user)
        return redirect(reverse("core:home"))

    except KaKaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(LoggedInOnlyView, DetailView):
    model = User
    context_object_name = "user_obj"


PROFILE_FIELDS = (
    ("first_name", "First Name"),
    ("last_name", "Last Name"),
    ("bio", "Bio"),
    ("gender", "Gender"),
    ("birth_date", "Birth Date"),
    ("language", "Language"),
    ("currency", "Currency"),
)


class UpdateProfileView(LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    models = User
    template_name = "users/update-profile.html"
    fields = tuple(map(lambda x: x[0], PROFILE_FIELDS))
    success_message = "Profile Updated"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        for field, label in PROFILE_FIELDS:
            form.fields[field].widget.attrs = {"placeholder": label}
        return form


PASSWORD_FIELDS = (
    ("old_password", "Current Password"),
    ("new_password1", "New Password"),
    ("new_password2", "Confirm New Password"),
)


class UpdatePasswordView(
    EmailLoginOnlyView,
    LoggedInOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):
    template_name = "users/update-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        for field, label in PASSWORD_FIELDS:
            form.fields[field].widget.attrs = {"placeholder": label}
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))
