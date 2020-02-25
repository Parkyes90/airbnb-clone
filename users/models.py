import uuid

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from config.settings import EMAIL_FROM


class User(AbstractUser):
    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_OTHER, _("Other")),
    )

    LANGUAGE_ENGLISH = _("en")
    LANGUAGE_KOREAN = _("kr")

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_KRW, "KRW"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, blank=True
    )
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES,
        max_length=2,
        blank=True,
        default=LANGUAGE_KOREAN,
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES,
        max_length=3,
        blank=True,
        default=CURRENCY_KRW,
    )
    super_host = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            send_mail(
                "Verify Airbnb Account",
                strip_tags(html_message),
                EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return
