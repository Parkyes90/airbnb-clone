from django.contrib import admin

from reservations import models


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Reservation Admin Definition"""

    pass
