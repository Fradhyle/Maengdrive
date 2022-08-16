from django.apps import AppConfig


class BusinessHoursConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "business_hours"
    verbose_name = "영업 시간 관리"
