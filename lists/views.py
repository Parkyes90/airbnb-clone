from django.shortcuts import redirect
from django.urls import reverse

from lists.models import List
from rooms.models import Room


def save_rooms(request, room_pk):
    room = Room.objects.get_or_none(pk=room_pk)
    if room is not None:
        the_list, _ = List.objects.get_or_create(
            user=request.user, name="My Favorites Houses"
        )
        the_list.rooms.add(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))
