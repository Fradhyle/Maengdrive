from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from branches.models import Branch


class Command(BaseCommand):
    help = "Initialize branch for developer accounts"

    def handle(self, *args, **kwargs):
        try:
            b = Branch(
                name="개발",
                postcode="16461",
                address1="경기도 수원시 팔달구 권선로 477",
                address2="102동 501호",
                phone1="010-2448-7150",
            )
            b.save()
        except IntegrityError:
            raise CommandError("무결성 조건 위반. DB를 확인 후 다시 시도하세요.")
        else:
            return self.stdout.write(self.style.SUCCESS("성공적으로 초기화 하였습니다."))
