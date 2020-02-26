from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView

from conversations.models import Conversation
from users.models import User


def go_conversation(request, a_pk, b_pk):
    user_one = User.objects.get_or_none(pk=a_pk)
    user_two = User.objects.get_or_none(pk=b_pk)
    if user_one is not None and user_two is not None:
        try:
            conversation = Conversation.objects.get(
                Q(participants=user_one) & Q(participants=user_two)
            )
        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create()
            conversation.participants.add(user_one, user_two)
        return redirect(
            reverse("conversations:detail", kwargs={"pk": conversation.pk})
        )


class ConversationDetailView(DetailView):
    model = Conversation
    template_name = "conversations/conversation_detail.html"
