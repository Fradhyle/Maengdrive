from django import forms
from django.forms import ModelChoiceField, ModelForm

from branches.models import Branch
from schedules.models import Schedule
from users.models import User


class ScheduleForm(ModelForm):
    def clean_user(self):
        user = self.cleaned_data["user"]
        return user

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

    user = ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        label="이용자",
        widget=forms.TextInput(
            attrs={
                "class": "form-select",
                "list": "user-list",
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
            # "user": forms.TextInput(
            #     attrs={
            #         "class": "form-control",
            #         "placeholder": "이용자 이름을 입력하세요.",
            #     },
            # ),
            "start_datetime": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "placeholder": "시작 시간을 입력하세요.",
                },
            ),
            "end_datetime": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "placeholder": "종료 시간을 입력하세요.",
                },
            ),
        }
