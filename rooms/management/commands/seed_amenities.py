from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):

    help = "This command creates amenities"

    def handle(self, *args, **options):
        amenities = [
            "주방",
            "샴푸",
            "난방",
            "에어컨",
            "세탁기",
            "건조기",
            "무선 인터넷",
            "아침식사",
            "실내 벽난로",
            "옷걸이",
            "다리미",
            "헤어드라이어",
            "노트북 작업 공간",
            "TV",
            "아기 침대",
            "유아용 식탁의자",
            "셀프 체크인",
            "화재 감지기",
            "일산화탄소 감지기",
            "욕실 단독 사용",
        ]
        for a in amenities:
            Amenity.objects.create(name=a)
        self.stdout.write(
            self.style.SUCCESS(f"{len(amenities)} amenities created!")
        )
