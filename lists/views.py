from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from lists.models import List
from rooms.models import Room


def toggle_room(request, room_pk):
    action = request.GET.get("action", None)

    room = Room.objects.get_or_none(pk=room_pk)
    if room is not None and action is not None:
        the_list, _ = List.objects.get_or_create(
            user=request.user, name="My Favorites Houses"
        )
        if action == "add":
            the_list.rooms.add(room)
        else:
            the_list.rooms.remove(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(TemplateView):
    template_name = "lists/list_detail.html"
