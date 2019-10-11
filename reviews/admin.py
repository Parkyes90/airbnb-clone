from django.contrib import admin

# Register your models here.
from reviews import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review Admin Definition"""

    pass
