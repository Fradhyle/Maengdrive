from django import forms
from django.forms import ModelChoiceField, ModelForm

from branches.models import Branch
from schedules.models import Schedule
from users.models import User


class ScheduleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ScheduleForm, self).__init__(*args, **kwargs)
        if self.user.superuser:
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

    class Meta:
        model = Schedule
        fields = (
            "branch",
            "user",
            "date",
            "period",
        )
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),
            "period": forms.NumberInput(
                attrs={
                    "class": "form-control",
                },
            ),
        }
