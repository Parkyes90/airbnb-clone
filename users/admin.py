from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from users import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """
        Custom User Admin
    """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birth_date",
                    "language",
                    "currency",
                    "super_host",
                )
            },
        ),
    )
