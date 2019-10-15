from django.core.management.base import BaseCommand
from rooms.models import HouseRule


class Command(BaseCommand):

    help = "This command creates house rules"

    def handle(self, *args, **options):
        house_rules = ["이벤트/행사 가능", "반려동물 입실 가능", "흡연 가능"]
        for h in house_rules:
            HouseRule.objects.create(name=h)
        self.stdout.write(
            self.style.SUCCESS(f"{len(house_rules)} house rules created!")
        )
