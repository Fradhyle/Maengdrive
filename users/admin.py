from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models

from users.models import User


# Register your models here.
@admin.action(description="선택한 이용자를 비활성화합니다")
def deactivate_user(modeladmin, request, queryset):
    queryset.update(active=False)


@admin.register(User)
class UserModelAdmin(UserAdmin):
    date_hierarchy = "date_joined"

    list_display = (
        "username",
        "name",
        "gender",
        "license_type",
        "plan_type",
        "branch",
        "active",
        "staff",
        "superuser",
        "date_joined",
    )

    list_display_links = ("username",)

    list_editable = (
        "name",
        "gender",
        "license_type",
        "plan_type",
        "branch",
        "active",
        "staff",
        "superuser",
    )

    list_filter = (
        "gender",
        "license_type",
        "plan_type",
        "branch",
        "active",
        "staff",
        "superuser",
    )

    fieldsets = (
        (
            "이용자 기본 정보",
            {
                "fields": (
                    "username",
                    "password",
                    "branch",
                    "license_type",
                    "plan_type",
                ),
            },
        ),
        (
            "개인 정보",
            {
                "fields": (
                    "name",
                    "birthday",
                    "gender",
                    "phone",
                ),
            },
        ),
        (
            "권한",
            {
                "fields": (
                    "staff",
                    "superuser",
                    "groups",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            "이용자 기본 정보",
            {
                "fields": (
                    "username",
                    "password",
                    "branch",
                    "license_type",
                    "plan_type",
                ),
            },
        ),
        (
            "개인 정보",
            {
                "fields": (
                    "name",
                    "birthday",
                    "gender",
                    "phone",
                ),
            },
        ),
        (
            "권한",
            {
                "fields": (
                    "staff",
                    "superuser",
                    "groups",
                ),
            },
        ),
    )

    search_fields = (
        "username",
        "name",
    )

    ordering = (
        "branch",
        "date_joined",
    )

    filter_horizontal = ()

    actions = (deactivate_user,)

    formfield_overrides = {
        models.TextField: {
            "widget": forms.TextInput(
                attrs={
                    "size": "6",
                },
            )
        },
    }
