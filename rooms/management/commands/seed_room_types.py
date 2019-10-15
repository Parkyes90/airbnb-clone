from django.core.management.base import BaseCommand
from rooms.models import RoomType


class Command(BaseCommand):

    help = "This command creates room types"

    def handle(self, *args, **options):
        room_types = ["주택", "아파트", "B & B", "부티크 호텔"]
        for r in room_types:
            RoomType.objects.create(name=r)
        self.stdout.write(
            self.style.SUCCESS(f"{len(room_types)} rooms types created!")
        )
