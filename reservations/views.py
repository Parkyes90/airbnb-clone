import datetime

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View

from reservations.models import BookedDay, Reservation
from rooms.models import Room


class CreateError(Exception):
    pass


def create(request, room, year, month, day):
    date_obj = datetime.datetime(year=year, month=month, day=day)
    try:
        room = Room.objects.get(pk=room)
        BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()
    except (Room.DoesNotExist, CreateError):
        messages.error(request, "Can't Reserve That Room")
        return redirect(reverse("core:home"))
    except BookedDay.DoesNotExist:
        reservation = Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            status=Reservation.STATUS_PENDING,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(
            reverse("reservations:detail", kwargs={"pk": reservation.pk})
        )


class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        reservation = Reservation.objects.get_or_none(pk=kwargs.get("pk"))
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()

        return render(
            self.request,
            "reservations/detail.html",
            {"reservation": reservation},
        )


def edit_reservation(request, pk, verb):
    reservation = Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
        reservation.guest != request.user
        and reservation.room.host != request.user
    ):
        raise Http404()
    if verb == "confirm":
        reservation.status = Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = Reservation.STATUS_CANCELED
        BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(
        reverse("reservations:detail", kwargs={"pk": reservation.pk})
    )
