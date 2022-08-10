from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models

from users.models import User


# Register your models here.
@admin.action(description="선택한 이용자를 비활성화")
def deactivate_user(queryset):
    queryset.update(is_active=False)


@admin.register(User)
class UserModelAdmin(ModelAdmin):
    date_hierarchy = "date_joined"

    list_display = (
        "username",
        "name",
        "gender",
        "license_type",
        "plan_type",
        "belong_to",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    list_display_links = ("username",)

    list_editable = (
        "name",
        "gender",
        "license_type",
        "plan_type",
        "belong_to",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    list_filter = (
        "gender",
        "license_type",
        "plan_type",
        "belong_to",
        "is_active",
        "is_staff",
        "is_superuser",
    )

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
