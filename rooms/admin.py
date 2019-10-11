from django.contrib import admin

from rooms import models


@admin.register(
    models.RoomType, models.Facility, models.Amenity, models.HouseRule
)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition"""

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """Room Admin Definition"""

    pass


@admin.register(models.Photo)
class PhoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition"""

    pass
