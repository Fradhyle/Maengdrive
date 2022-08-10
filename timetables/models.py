import datetime

from django.db import models
from django.urls import reverse

from branches.models import Branch


# Create your models here.
class Timetable(models.Model):
    srl = models.BigAutoField(
        primary_key=True,
        verbose_name="연번",
    )
    branch_srl = models.ForeignKey(
        "branches.Branch",
        on_delete=models.DO_NOTHING,
        verbose_name="지점 연번",
    )
    period = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        verbose_name="교시",
    )
    period_length = models.DurationField(
        default=datetime.timedelta(minutes=50),
        verbose_name="수업 시간",
    )
    is_holiday = models.BooleanField(
        default=False,
        verbose_name="휴일 여부",
    )
    start_time = models.TimeField(
        default=datetime.time(10, 00),
        verbose_name="시작 시간",
    )
    end_time = models.TimeField(
        default=datetime.time(23, 00),
        verbose_name="종료 시간",
    )

    class Meta:
        verbose_name = "시간표"
        verbose_name_plural = "시간표"
        ordering = ["branch_srl", "period"]

    def __str__(self):
        branch_name = Branch.objects.get(srl=self.branch_srl)
        return branch_name + " " + self.period + "교시"

    # def get_absolute_url(self):
    #     return reverse("timetable:index", kwargs={"srl": self.srl})
