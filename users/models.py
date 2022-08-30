from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group
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
        self,
        username,
        full_name,
        birthday,
        gender,
        phone,
        branch,
        password=None,
        **kwargs,
    ):
        user = self.model(
            username=username,
            full_name=full_name,
            group=Group.objects.get_or_create(name="회원"),
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
        self, username, full_name, birthday, gender, phone, branch, password, **kwargs
    ):
        user = self.create_user(
            username, full_name, birthday, gender, phone, branch, password, kwargs
        )
        user.staff = True
        user.group = (Group.objects.get_or_create(name="직원"),)
        user.save(using=self._db)

        return user

    def create_superuser(
        self, username, full_name, birthday, gender, phone, branch, password, **kwargs
    ):
        user = self.create_user(
            username, full_name, birthday, gender, phone, branch, password, kwargs
        )
        user.staff = True
        user.superuser = True
        user.group = (Group.objects.get_or_create(name="최고관리자"),)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    objects = UserManager()

    GENDERS = (
        (None, "미선택"),
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
    full_name = models.TextField(
        verbose_name="이름",
    )
    password = models.TextField(
        verbose_name="비밀번호",
    )
    groups = models.ManyToManyField(
        to=Group,
        verbose_name="그룹",
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
    branch = models.ForeignKey(
        "branches.Branch",
        verbose_name="소속 지점",
        on_delete=models.DO_NOTHING,
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
    staff = models.BooleanField(
        verbose_name="직원 여부",
        default=False,
    )
    active = models.BooleanField(
        verbose_name="활성 상태",
        default=True,
    )
    superuser = models.BooleanField(
        verbose_name="최고관리자 여부",
        default=False,
    )
    last_login = models.DateTimeField(
        verbose_name="최종 접속 일시",
        default=timezone.now,
    )
    date_joined = models.DateTimeField(
        verbose_name="가입 일시",
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

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_superuser(self):
        return self.superuser

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission, where perm is in the format "<app label>.<permission codename>". (see documentation on permissions).
        If the user is inactive, this method will always return False. For an active superuser, this method will always return True.

        If obj is passed in, this method won’t check for a permission for the model, but for this specific object.
        """

        return self.staff

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions, where each perm is in the format "<app label>.<permission codename>".
        If the user is inactive, this method will always return False. For an active superuser, this method will always return True.

        If obj is passed in, this method won’t check for permissions for the model, but for the specific object.
        """
        print(perm_list)
        permissions = []
        for group in self.groups.all():
            permissions.extend(group.permissions.all())
        print(self.groups.all()[0].permissions.filter(codename="add_schedules"))
        # print(Group.objects.filter(name=self.groups))

        return self.staff

    def has_module_perms(self, package_name):
        """
        Returns True if the user has any permissions in the given package (the Django app label).
        If the user is inactive, this method will always return False.
        For an active superuser, this method will always return True.
        """
        if self.active == False:
            return False
        elif self.active == True:
            return self.staff

    class Meta:
        verbose_name = "이용자"
        verbose_name_plural = "이용자"
        ordering = [
            "branch",
            "srl",
        ]

    def __str__(self):
        if self.gender == "M":
            gender_short = "남"
        elif self.gender == "F":
            gender_short = "여"

        return f"{self.full_name} ({self.branch}/{self.birthday.strftime('%y%m%d')}/{gender_short})"

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"srl": self.srl})
