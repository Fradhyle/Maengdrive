from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models

from schedules.models import Schedule


# Register your models here.
@admin.register(Schedule)
class ScheduleAdmin(ModelAdmin):
    date_hierarchy = "date"

    list_display = (
        "srl",
        "branch",
        "user",
        "date",
        "period",
    )

    list_display_links = ("srl",)

    list_editable = (
        "branch",
        "user",
        "date",
        "period",
    )

    list_filter = (
        "branch",
        "user",
        "date",
        "period",
    )
