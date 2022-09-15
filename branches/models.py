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
    name = models.CharField(
        verbose_name="지점명",
        unique=True,
        max_length=255,
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
    address1 = models.CharField(
        verbose_name="도로명 주소",
        max_length=255,
    )
    address2 = models.CharField(
        verbose_name="상세 주소",
        blank=True,
        max_length=255,
    )
    phone1 = models.CharField(
        verbose_name="전화번호 1",
        max_length=14,
        validators=[
            phone_validator,
        ],
    )
    phone2 = models.CharField(
        verbose_name="전화번호 2",
        max_length=14,
        validators=[
            phone_validator,
        ],
        blank=True,
    )
    closure = models.BooleanField(
        verbose_name="폐업 여부",
        default=False,
        choices=(
            (None, "미선택"),
            (False, "개업"),
            (True, "폐업"),
        ),
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


class Hour(models.Model):
    srl = models.BigAutoField(
        verbose_name="연번",
        primary_key=True,
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
        if self.is_holiday:
            holiday = "휴일"
        else:
            holiday = "평일"

        return f"{self.branch.name} {holiday} {self.open_time} ~ {self.close_time}"

    # def get_absolute_url(self):
    #     return reverse("branches:hours", kwargs={"branch": self.branch.srl})


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
        if self.is_holiday:
            holiday = "휴일"
        else:
            holiday = "평일"

        return f"{self.branch.name} {holiday} {self.period}교시"

    # def get_absolute_url(self):
    #     return reverse("timetables:detail", kwargs={"branch": self.branch.srl})
