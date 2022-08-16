from django.contrib import admin
from django.contrib.admin import ModelAdmin

from timetables.models import Timetable


# Register your models here.
@admin.register(Timetable)
class TimetableModelAdmin(ModelAdmin):
    list_display = (
        "srl",
        "branch",
        "is_holiday",
        "period",
        "start_time",
        "end_time",
    )
    list_display_links = ("srl",)
    list_editable = (
        "branch",
        "is_holiday",
        "period",
        "start_time",
        "end_time",
    )
    list_filter = (
        "branch",
        "is_holiday",
    )