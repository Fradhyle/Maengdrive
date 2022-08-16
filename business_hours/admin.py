from django.contrib import admin
from django.contrib.admin import ModelAdmin

from business_hours.models import BusinessHours


# Register your models here.
@admin.register(BusinessHours)
class TimetableModelAdmin(ModelAdmin):
    list_display = (
        "srl",
        "branch",
        "is_holiday",
        "open_time",
        "close_time",
    )
    list_display_links = ("srl",)
    list_editable = (
        "branch",
        "is_holiday",
        "open_time",
        "close_time",
    )
    list_filter = (
        "branch",
        "is_holiday",
    )
