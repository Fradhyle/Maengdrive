from re import L

from django import forms
from django.forms import ModelChoiceField, ModelForm

from branches.models import Branch
from schedules.models import Schedule
from users.models import User


class ScheduleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ScheduleForm, self).__init__(*args, **kwargs)
        if self.user.is_superuser:
            self.fields["branch"] = ModelChoiceField(
                queryset=Branch.objects.all(),
                required=True,
                label="지점",
                widget=forms.Select(
                    attrs={
                        "class": "form-select",
                    }
                ),
            )
            self.fields["user"] = ModelChoiceField(
                queryset=User.objects.all(),
                required=True,
                label="이용자",
                widget=forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "list": "user-list",
                    }
                ),
            )
        else:
            self.fields["branch"] = ModelChoiceField(
                queryset=Branch.objects.filter(branch=self.user.branch),
                required=True,
                label="지점",
                widget=forms.Select(
                    attrs={
                        "class": "form-select",
                    }
                ),
            )
            self.fields["user"] = ModelChoiceField(
                queryset=User.objects.filter(branch=self.user.branch),
                required=True,
                label="이용자",
                widget=forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "list": "user-list",
                    }
                ),
            )

    def clean_user(self):
        user = self.cleaned_data["user"]
        print(user)

        return user

    class Meta:
        model = Schedule
        fields = (
            "start_datetime",
            "end_datetime",
        )
        widgets = {
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
