from django import forms
from django.forms import ModelForm

from schedules.models import Schedule


class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = []
        labels = {}
        widgets = {}
