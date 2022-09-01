import datetime

from django import forms
from django.forms import ModelChoiceField, ModelForm

from branches.models import Branch
from schedules.models import Schedule
from timetables.models import Timetable
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

    def clean(self):
        cleaned_data = super(ScheduleForm, self).clean()
        print(locals())
        print(cleaned_data)
        user_input = cleaned_data["user"]
        name = user_input.split(" ")[0]
        user_info = user_input.split(" ")[1]
        user_info = user_info.strip("()")
        user_info = user_info.split("/")
        branch = Branch.objects.get(name=user_info[0])
        birthday = datetime.datetime.strptime(user_info[1], "%y%m%d")
        if user_info[2] == "남":
            gender = "M"
        else:
            gender = "F"
        user = User.objects.get(
            name=name,
            birthday=birthday,
            gender=gender,
            branch=branch,
        )
        cleaned_data["user"] = user
        return cleaned_data

    class Meta:
        model = Schedule
        fields = (
            "branch",
            "user",
            "date",
            "period",
        )
        widgets = {
            "user": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "list": "user-list",
                },
            ),
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),
            "period": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                },
            ),
        }
