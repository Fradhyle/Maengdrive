from django.db import models

# Create your models here.
class Timetable(models.Model):
    period = models.DecimalField(max_digits=2, decimal_places=0, verbose_name="교시")
    is_holiday = models.BooleanField(default=False, verbose_name="휴일 여부")
    start_time = models.TimeField(verbose_name="시작 시간")
    end_time = models.TimeField(verbose_name="종료 시간")

class Schedule(models.Model):
    srl = models.BigAutoField(primary_key=True, verbose_name="연번")
    user_srl = models.ForeignKey("users.User", to_field="srl", on_delete=models.CASCADE, verbose_name="이용자 연번")
    branch_srl = models.ForeignKey("branches.Branch", to_field="srl", on_delete=models.DO_NOTHING, verbose_name="지점 연번")
    start_datetime = models.DateTimeField(verbose_name="시작 일시")
    end_datetime = models.DateTimeField(verbose_name="종료 일시")