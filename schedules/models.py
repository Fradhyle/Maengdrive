from django.conf import settings
from django.db import models


# Create your models here.
class Schedule(models.Model):
    srl = models.BigAutoField(
        primary_key=True,
        verbose_name="연번",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        verbose_name="이용자",
    )
    branch = models.ForeignKey(
        "branches.Branch",
        on_delete=models.DO_NOTHING,
        verbose_name="지점",
    )
    start_datetime = models.DateTimeField(
        verbose_name="시작 일시",
    )
    end_datetime = models.DateTimeField(
        verbose_name="종료 일시",
    )

    class Meta:
        verbose_name = "일정"
        verbose_name_plural = "일정"
        ordering = [
            "branch",
            "start_datetime",
        ]

    # def __str__(self):
    #     branch_name = Branch.objects.get(srl=self.branch_srl)
    #     return branch_name +  + self.period + "교시"

    # def get_absolute_url(self):
    #     return reverse("timetable:index", kwargs={"srl": self.srl})
