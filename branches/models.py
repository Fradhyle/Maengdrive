import datetime

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

# Create your models here.
phone_validator = RegexValidator(
    regex="\d{2,4}-?\d{3,4}(-?\d{4})?",
    message="올바른 전화번호 형식이 아닙니다.",
)


class Branch(models.Model):
    srl = models.BigAutoField(
        verbose_name="연번",
        primary_key=True,
    )
    name = models.TextField(
        verbose_name="지점명",
        unique=True,
    )
    equipment_count = models.DecimalField(
        verbose_name="장비 대수",
        max_digits=2,
        decimal_places=0,
        default=5,
    )
    postcode = models.CharField(
        verbose_name="우편번호",
        max_length=5,
    )
    address1 = models.TextField(
        verbose_name="도로명 주소",
    )
    address2 = models.TextField(
        verbose_name="상세 주소",
        blank=True,
    )
    phone1 = models.CharField(
        verbose_name="전화번호 1",
        max_length=13,
        validators=[
            phone_validator,
        ],
    )
    phone2 = models.CharField(
        verbose_name="전화번호 2",
        max_length=13,
        validators=[
            phone_validator,
        ],
        blank=True,
    )
    closure = models.BooleanField(
        verbose_name="폐업 여부",
        default=False,
    )
    weekday_open_time = models.TimeField(
        verbose_name="평일 개점 시간",
        default=datetime.time(9, 0),
    )
    weekday_close_time = models.TimeField(
        verbose_name="평일 폐점 시간",
        default=datetime.time(23, 0),
    )
    holiday_open_time = models.TimeField(
        verbose_name="휴일 개점 시간",
        default=datetime.time(10, 0),
    )
    holiday_close_time = models.TimeField(
        verbose_name="휴일 폐점 시간",
        default=datetime.time(22, 0),
    )
    lesson_time = models.DurationField(
        verbose_name="수업 시간",
        default=datetime.timedelta(minutes=110),
    )
    break_time = models.DurationField(
        verbose_name="쉬는 시간",
        default=datetime.timedelta(minutes=10),
    )

    class Meta:
        verbose_name = "지점"
        verbose_name_plural = "지점"
        ordering = [
            "srl",
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("branches:detail", kwargs={"srl": self.srl})
