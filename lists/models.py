from django.db import models

# Create your models here.
from core.models import TimeStampedModel


class List(TimeStampedModel):
    """ List Model Definition"""

    name = models.CharField(max_length=80)
    user = models.ForeignKey(
        "users.User", related_name="lists", on_delete=models.CASCADE
    )
    rooms = models.ManyToManyField(
        "rooms.Room", related_name="lists", blank=True
    )

    def __str__(self):
        return self.name
