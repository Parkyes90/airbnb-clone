from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from reviews.forms import CreateReviewForm
from rooms.models import Room


def create_review(request, room):
    if request.method == "POST":
        form = CreateReviewForm(request.POST)
        room = Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, "Room reviewed")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
