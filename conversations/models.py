from django.db import models

# Create your models here.
from core.models import TimeStampedModel


class Conversation(TimeStampedModel):
    participants = models.ManyToManyField(
        "users.User", related_name="conversations", blank=True
    )

    def __str__(self):
        user_names = []
        for user in self.participants.all():
            user_names.append(user.username)
        return ", ".join(user_names)

    def count_messages(self):
        return self.messages.count()

    def count_participants(self):
        return self.participants.count()

    count_messages.short_description = "Number of Messages"
    count_participants.short_description = "Number Of Participants"


class Message(TimeStampedModel):
    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=True
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"
