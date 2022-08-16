from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
)
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from branches.models import Branch

# Create your models here.
phone_validator = RegexValidator(
    regex="\d{2,4}-?\d{3,4}(-?\d{4})?",
    message="올바른 전화번호 형식이 아닙니다.",
)


class UserManager(BaseUserManager):
    def create_user(
        self, username, name, birthday, gender, phone, branch, password=None, **kwargs
    ):
        user = self.model(
            username=username,
            name=name,
            birthday=birthday,
            gender=gender,
            phone=phone,
            license_type=kwargs["license_type"],
            plan_type=kwargs["plan_type"],
            branch=Branch.objects.get(srl=branch),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staff(
        self, username, name, birthday, gender, phone, branch, password, **kwargs
    ):
        user = self.create_user(
            username, name, birthday, gender, phone, branch, password, kwargs
        )
        user.is_staff = True
        user.save(using=self._db)

        return user

    def create_superuser(
        self, username, name, birthday, gender, phone, branch, password, **kwargs
    ):
        user = self.create_user(
            username, name, birthday, gender, phone, branch, password, kwargs
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    GENDERS = (
        ("M", "남성"),
        ("F", "여성"),
    )
    LICENSE_TYPES = (
        (None, "미선택"),
        ("1L", "1종 대형"),
        ("1O", "1종 보통"),
        ("1OA", "1종 보통 (자동)"),
        ("2O", "2종 보통"),
        ("2OA", "2종 보통 (자동)"),
        ("P", "장롱 면허"),
    )
    PLAN_TYPES = (
        (None, "미선택"),
        ("T", "시간제"),
        ("G", "합격보장제"),
        ("P", "장롱 면허"),
    )
    srl = models.BigAutoField(
        primary_key=True,
        verbose_name="연번",
    )
    username = models.TextField(
        unique=True,
        verbose_name="아이디",
    )
    name = models.TextField(
        verbose_name="이름",
    )
    birthday = models.DateField(
        verbose_name="생년월일",
    )
    gender = models.TextField(
        verbose_name="성별",
        choices=GENDERS,
    )
    phone = models.TextField(
        verbose_name="전화번호",
        validators=(phone_validator,),
    )
    license_type = models.CharField(
        max_length=3,
        verbose_name="면허 종류",
        choices=LICENSE_TYPES,
        blank=True,
        null=True,
        default=None,
    )
    plan_type = models.CharField(
        max_length=1,
        verbose_name="요금제 유형",
        choices=PLAN_TYPES,
        blank=True,
        null=True,
        default=None,
    )
    branch = models.ForeignKey(
        "branches.Branch",
        verbose_name="소속 지점",
        on_delete=models.DO_NOTHING,
    )
    is_active = models.BooleanField(
        verbose_name="활성 상태",
        default=True,
    )
    is_staff = models.BooleanField(
        verbose_name="직원 여부",
        default=False,
    )
    is_superuser = models.BooleanField(
        verbose_name="최고관리자 여부",
        default=False,
    )
    date_joined = models.DateTimeField(
        verbose_name="가입일",
        default=timezone.now,
    )

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = (
        "name",
        "birthday",
        "gender",
        "phone",
        "branch",
    )

    class Meta:
        verbose_name = "이용자"
        verbose_name_plural = "이용자"

    def __str__(self):
        if self.gender == "M":
            gender_short = "남"
        elif self.gender == "F":
            gender_short = "여"

        return f"{self.name} ({self.branch}/{self.birthday.strftime('%y%m%d')}/{gender_short})"

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"srl": self.srl})


class BranchViewPermission(Permission):
    name = "지점 정보를 볼 수 있음"
    content_type = ContentType(app_label="users", model="user")
    codename = "can_view_branch"


class MemberGroup(Group):
    name = "회원"


class StaffGroup(Group):
    name = "직원"


class ManagerGroup(Group):
    name = "매니저"


class SuperuserGroup(Group):
    name = "최고 관리자"
