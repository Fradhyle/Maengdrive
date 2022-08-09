from django import forms
from django.forms import ModelChoiceField, ModelForm

from branches.models import Branch
from schedules.models import Schedule, Timetable


class TimetableForm(ModelForm):
    branch_srl = ModelChoiceField(
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
        model = Timetable
        fields = (
            "branch_srl",
            "period",
            "period_length",
            "is_holiday",
            "start_time",
            "end_time",
        )
        widgets = {
            "period": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "몇 교시인지 입력하세요.",
                },
            ),
            "period_length": forms.TimeInput(
                format="%H:%M:%S",
                attrs={
                    "class": "form-control",
                    "placeholder": "해당 교시의 길이를 입력하세요.",
                },
            ),
            "is_holiday": forms.RadioSelect(
                choices=[(True, "예"), (False, "아니오")],
                attrs={
                    "class": "form-check-input",
                },
            ),
            "start_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                    "placeholder": "교시 시작 시간을 입력하세요.",
                },
            ),
            "end_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                    "placeholder": "교시 종료 시간을 입력하세요.",
                },
            ),
        }


class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = []
        labels = {}
        widgets = {}
