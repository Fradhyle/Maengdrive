from django import forms
from django.contrib import admin
from django.db import models

from branches.models import Branch


# Register your models here.
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "equipment_count",
        "postcode",
        "address1",
        "address2",
        "phone1",
        "phone2",
        "closure",
    )

    list_display = (
        "srl",
        "name",
        "equipment_count",
        "phone1",
        "phone2",
        "closure",
    )

    list_display_links = ("name",)

    list_editable = (
        "equipment_count",
        "phone1",
        "phone2",
        "closure",
    )

    list_filter = ("closure",)
