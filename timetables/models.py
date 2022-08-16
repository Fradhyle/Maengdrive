from django.db import models
from django.urls import reverse

from branches.models import Branch


# Create your models here.
class Timetable(models.Model):
    srl = models.BigAutoField(
        primary_key=True,
        verbose_name="연번",
    )
    branch = models.ForeignKey(
        "branches.Branch",
        on_delete=models.CASCADE,
        verbose_name="지점",
    )
    is_holiday = models.BooleanField(
        verbose_name="휴일 여부",
    )
    period = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        verbose_name="교시",
    )
    start_time = models.TimeField(
        verbose_name="시작 시간",
    )
    end_time = models.TimeField(
        verbose_name="종료 시간",
    )

    class Meta:
        verbose_name = "시간표"
        verbose_name_plural = "시간표"
        ordering = [
            "branch",
            "is_holiday",
            "period",
        ]
        unique_together = [
            "branch",
            "is_holiday",
            "period",
        ]

    def __str__(self):
        branch_name = Branch.objects.get(srl=self.branch.srl).name
        if self.is_holiday:
            holiday = "휴일"
        else:
            holiday = "평일"

        return f"{branch_name} {holiday} {self.period}교시"

    def get_absolute_url(self):
        return reverse("timetables:detail", kwargs={"branch": self.branch.srl})