import datetime

from django.db import models
from django.urls import reverse

from branches.models import Branch


# Create your models here.
class BusinessHours(models.Model):
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
    open_time = models.TimeField(
        verbose_name="개점 시간",
        default=datetime.time(9, 0),
    )
    close_time = models.TimeField(
        verbose_name="폐점 시간",
        default=datetime.time(23, 0),
    )

    class Meta:
        verbose_name = "영업 시간"
        verbose_name_plural = "영업 시간"
        ordering = [
            "branch",
            "is_holiday",
            "open_time",
        ]
        unique_together = [
            "branch",
            "is_holiday",
        ]

    def __str__(self):
        branch_name = Branch.objects.get(srl=self.branch.srl).name
        if self.is_holiday:
            holiday = "휴일"
        else:
            holiday = "평일"

        return f"{branch_name} {holiday} {self.open_time} ~ {self.close_time}"

    def get_absolute_url(self):
        return reverse("business_hours:detail", kwargs={"branch": self.branch.srl})
