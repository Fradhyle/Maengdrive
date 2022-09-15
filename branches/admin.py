from django import forms
from django.contrib import admin
from django.db import models

from branches.models import Branch, Hour, Timetable


# Register your models here.
@admin.action(description="선택한 지점을 폐업 처리합니다")
def branch_close(modeladmin, request, queryset):
    queryset.update(closure=True)


@admin.action(description="선택한 지점을 개업 처리합니다")
def branch_open(modeladmin, request, queryset):
    queryset.update(closure=False)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = (
        "srl",
        "name",
        "phone1",
        "phone2",
        "closure",
    )

    list_display_links = ("name",)

    list_filter = ("closure",)

    fieldsets = (
        (
            "기본 정보",
            {
                "fields": (
                    "name",
                    "equipment_count",
                    "closure",
                ),
            },
        ),
        (
            "주소",
            {
                "fields": (
                    "address1",
                    "address2",
                ),
            },
        ),
        (
            "연락처",
            {
                "fields": (
                    "phone1",
                    "phone2",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            "기본 정보",
            {
                "fields": (
                    "name",
                    "equipment_count",
                    "closure",
                ),
            },
        ),
        (
            "주소",
            {
                "fields": (
                    "address1",
                    "address2",
                ),
            },
        ),
        (
            "연락처",
            {
                "fields": (
                    "phone1",
                    "phone2",
                ),
            },
        ),
    )

    search_fields = ("name",)

    ordering = ("srl",)

    filter_horizontal = ()

    actions = (
        branch_close,
        branch_open,
    )


@admin.register(Hour)
class HourAdmin(admin.ModelAdmin):
    fields = (
        "branch",
        "is_holiday",
        "open_time",
        "close_time",
    )

    list_display = (
        "srl",
        "branch",
        "is_holiday",
        "open_time",
        "close_time",
    )

    list_display_links = (
        "srl",
        "branch",
    )

    list_editable = (
        "is_holiday",
        "open_time",
        "close_time",
    )

    list_filter = (
        "branch",
        "is_holiday",
        "open_time",
        "close_time",
    )


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
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
