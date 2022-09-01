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
        on_delete=models.CASCADE,
        verbose_name="이용자",
    )
    branch = models.ForeignKey(
        "branches.Branch",
        on_delete=models.CASCADE,
        verbose_name="지점",
    )
    date = models.DateField(
        verbose_name="일자",
    )
    period = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        verbose_name="교시",
    )

    class Meta:
        verbose_name = "일정"
        verbose_name_plural = "일정"
        ordering = [
            "branch",
            "date",
            "period",
        ]
        unique_together = [
            "user",
            "date",
            "period",
        ]

    def __str__(self):
        if self.user.gender == "M":
            gender_short = "남"
        elif self.user.gender == "F":
            gender_short = "여"

        return f"{self.branch} {self.date.strftime('%y%m%d')} {self.period}교시 {self.user.name}{self.user.birthday.strftime('%y%m%d')}{gender_short}"

    # def get_absolute_url(self):
    #     return reverse("timetable:index", kwargs={"srl": self.srl})
