from django import forms
from django.forms import ModelChoiceField, ModelForm

from branches.models import Branch
from business_hours.models import BusinessHours


class BusinessHoursForm(ModelForm):
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
        model = BusinessHours
        fields = (
            "branch",
            "is_holiday",
            "open_time",
            "close_time",
        )
        widgets = {
            "is_holiday": forms.RadioSelect(
                choices=[(True, "예"), (False, "아니오")],
                attrs={
                    "class": "form-check-input",
                },
            ),
            "open_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                    "placeholder": "개점 시간을 입력하세요.",
                },
            ),
            "close_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                    "placeholder": "폐점 시간을 입력하세요.",
                },
            ),
        }
