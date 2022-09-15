import datetime

from django import forms
from django.forms import ModelChoiceField, ModelForm

from branches.models import Branch, Timetable
from schedules.models import Schedule
from users.models import User


class ScheduleForm(ModelForm):
    user = forms.CharField(
        label="이용자",
        widget=forms.TextInput(
            attrs={
                "class": "form-select",
                "list": "user-list",
                "placeholder": "이름을 입력한 후 올바른 이용자를 선택하세요.",
            },
        ),
        required=True,
    )

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
            max_period = Timetable.objects.all().order_by("-period")[0].period
            self.fields["period"] = forms.DecimalField(
                label="교시",
                min_value=1,
                max_value=max_period,
                max_digits=2,
                decimal_places=1,
                step_size=0.5,
                widget=forms.NumberInput(
                    attrs={
                        "class": "form-control",
                        "min": 1,
                        "step": 0.5,
                        "max": max_period,
                    },
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
            max_period = (
                Timetable.objects.filter(branch=self.user.branch)
                .order_by("-period")[0]
                .period
            )
            self.fields["period"] = forms.DecimalField(
                label="교시",
                min_value=1,
                max_value=max_period,
                max_digits=2,
                decimal_places=1,
                step_size=0.5,
                widget=forms.NumberInput(
                    attrs={
                        "class": "form-control",
                        "min": 1,
                        "step": 0.5,
                        "max": max_period,
                    },
                ),
            )

    def clean_user(self):
        user_input = self.cleaned_data["user"]
        name = user_input.split(" ")[0]
        user_info = user_input.split(" ")[1]
        user_info = user_info.strip("()").split("/")
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

        return user

    class Meta:
        model = Schedule
        fields = (
            "user",
            "branch",
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
        }
