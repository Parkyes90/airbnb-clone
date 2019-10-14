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

    list_filter = UserAdmin.list_filter + ("super_host",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "super_host",
        "is_staff",
        "is_superuser",
    )
