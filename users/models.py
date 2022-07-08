from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self):
        pass

    def create_superuser(self):
        pass


class User(AbstractBaseUser):
    GENDER_TYPES = [
        ("M", "남성"),
        ("F", "여성"),
    ]
    LICENSE_TYPES = [
        ("", ""),
        ("L1L", "1종 대형"),
        ("L1G", "1종 보통"),
        ("L1GA", "1종 보통 (자동)"),
        ("L2G", "2종 보통"),
        ("L2GA", "2종 보통 (자동)"),
        ("P", "장롱 면허"),
    ]
    PLAN_TYPES = [
        ("", ""),
        ("T", "시간제"),
        ("G", "합격보장제"),
        ("P", "장롱 면허"),
    ]
    srl = models.BigAutoField(primary_key=True, verbose_name="이용자 연번")
    username = models.TextField(unique=True, verbose_name="이용자 아이디")
    name = models.TextField(verbose_name="이름")
    birthday = models.DateField(verbose_name="생년월일")
    gender = models.TextField(verbose_name="성별", choices=GENDER_TYPES)
    phone = models.TextField(verbose_name="전화번호")
    license_type = models.TextField(
        verbose_name="면허 종류", choices=LICENSE_TYPES, null=True)
    plan_type = models.TextField(
        verbose_name="요금제 유형", choices=PLAN_TYPES, null=True)
    belong_to = models.ForeignKey(
        "branches.Branch",
        to_field="srl",
        verbose_name="소속 지점",
        on_delete=models.DO_NOTHING,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "name",
        "birthday",
        "phone",
        "license_type",
        "plan_type",
        "belong_to",
        "is_staff",
        "is_active",
        "date_joined"
    ]

    class Meta:
        verbose_name = "이용자"

    def __str__(self):
        name = self.name
        birthday = self.birthday.strftime("%y%m%d")
        gender = self.gender
        return name + " (" + birthday + gender + ")"
