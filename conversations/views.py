from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View

from conversations.forms import AddCommentForm
from conversations.models import Conversation, Message
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


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404
        form = AddCommentForm()
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation, "form": form},
        )

    def post(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404
        form = AddCommentForm(self.request.POST)
        if form.is_valid():
            Message.objects.create(
                user=self.request.user,
                **form.cleaned_data,
                conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
