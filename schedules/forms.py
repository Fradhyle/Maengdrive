from django import forms
from django.forms import ModelChoiceField, ModelForm

from branches.models import Branch
from schedules.models import Schedule


class ScheduleForm(ModelForm):
    branch = ModelChoiceField(
        queryset=Branch.objects.all(),
        required=True,
        label="지점",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            },
        ),
    )

    class Meta:
        model = Schedule
        fields = (
            "user",
            "branch",
            "start_datetime",
            "end_datetime",
        )
        widgets = {
            "user": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "이용자 이름을 입력하세요.",
                },
            ),
            "start_datetime": forms.DateTimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                    "placeholder": "시작 시간을 입력하세요.",
                },
            ),
            "end_datetime": forms.DateTimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                    "placeholder": "종료 시간을 입력하세요.",
                },
            ),
        }
