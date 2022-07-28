from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
phone_validator = RegexValidator(
    regex="\d{2,3}-?\d{3,4}-?\d{4}", message="올바른 전화번호 형식이 아닙니다."
)
postcode_validator = RegexValidator(regex="\d{5}", message="올바른 우편번호 형식이 아닙니다.")


class Branch(models.Model):
    srl = models.BigAutoField(primary_key=True, verbose_name="연번")
    name = models.TextField(verbose_name="지점명")
    postcode = models.CharField(
        max_length=5, validators=[postcode_validator], verbose_name="우편번호"
    )
    address1 = models.TextField(verbose_name="도로명 주소")
    address2 = models.TextField(verbose_name="상세 주소", blank=True)
    phone1 = models.CharField(
        max_length=13, validators=[phone_validator], verbose_name="전화번호 1"
    )
    phone2 = models.CharField(
        max_length=13, validators=[phone_validator], verbose_name="전화번호 2"
    )
    is_opened = models.BooleanField(default=True, verbose_name="운영 여부")

    class Meta:
        verbose_name = "지점"

    def __str__(self):
        return self.name
