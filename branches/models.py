from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
phone_validator = RegexValidator(regex="\d{2,3}-?\d{3,4}-?\d{4}", message="올바른 전화번호 형식이 아닙니다.")

class Branch(models.Model):
    srl = models.BigAutoField(primary_key=True, verbose_name="연번")
    name = models.TextField(verbose_name="지점명")
    address = models.TextField(verbose_name="주소")
    phone1 = models.TextField(validators=[phone_validator], verbose_name="전화번호 1")
    phone2 = models.TextField(validators=[phone_validator], verbose_name="전화번호 2")
    
    class Meta:
        verbose_name = "지점"
    
    def __str__(self):
        return self.name
