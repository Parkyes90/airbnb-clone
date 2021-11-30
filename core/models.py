from django.db import models

from core.managers import CustomModelManager


class TimeStampedModel(models.Model):
    """
        Time Stamp Model
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = CustomModelManager()

    class Meta:
        abstract = True
