import datetime

from django.conf import settings
from django.db import models


# Create your models here.
class Timetable(models.Model):
    srl = models.BigAutoField(
        primary_key=True,
        verbose_name="연번",
    )
    branch_srl = models.ForeignKey(
        "branches.Branch",
        on_delete=models.CASCADE,
        verbose_name="지점 연번",
    )
    period = models.DecimalField(max_digits=2, decimal_places=0, verbose_name="교시")
    period_length = models.DurationField(
        default=datetime.timedelta(minutes=50), verbose_name="수업 시간"
    )
    is_holiday = models.BooleanField(default=False, verbose_name="휴일 여부")
    start_time = models.TimeField(default=datetime.time(10, 00), verbose_name="시작 시간")
    end_time = models.TimeField(default=datetime.time(11, 00), verbose_name="종료 시간")


class Schedule(models.Model):
    srl = models.BigAutoField(
        primary_key=True,
        verbose_name="연번",
    )
    user_srl = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="이용자 연번",
    )
    branch_srl = models.ForeignKey(
        "branches.Branch",
        on_delete=models.DO_NOTHING,
        verbose_name="지점 연번",
    )
    start_datetime = models.DateTimeField(
        verbose_name="시작 일시",
    )
    end_datetime = models.DateTimeField(
        verbose_name="종료 일시",
    )
