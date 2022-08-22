from django import forms
from django.forms import ModelChoiceField, ModelForm

from branches.models import Branch
from users.models import User


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(UserForm, self).__init__(*args, **kwargs)
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

    def clean_phone(self, field_name):
        phone_number = self.cleaned_data.get(field_name)
        phone_number = phone_number.replace("-", "")

        if len(phone_number) == 0:
            return phone_number
        elif phone_number[0:2] == "02" and len(phone_number) == 9:
            phone_number = [phone_number[0:2], phone_number[2:5], phone_number[5:]]
            phone_number = "-".join(phone_number)
        elif phone_number[0:2] == "02" and len(phone_number) == 10:
            phone_number = [phone_number[0:2], phone_number[2:6], phone_number[6:]]
            phone_number = "-".join(phone_number)
        elif phone_number[0] != 0 and len(phone_number) == 8:
            phone_number = [phone_number[0:4], phone_number[4:]]
            phone_number = "-".join(phone_number)
        elif len(phone_number) == 10:
            phone_number = [phone_number[0:3], phone_number[3:6], phone_number[6:]]
            phone_number = "-".join(phone_number)
        elif len(phone_number) == 11:
            phone_number = [phone_number[0:3], phone_number[3:7], phone_number[7:]]
            phone_number = "-".join(phone_number)

        return phone_number

    class Meta:
        GENDERS = (
            ("M", "남성"),
            ("F", "여성"),
        )
        LICENSE_TYPES = (
            (None, "미선택"),
            ("1L", "1종 대형"),
            ("1O", "1종 보통"),
            ("1OA", "1종 보통 (자동)"),
            ("2O", "2종 보통"),
            ("2OA", "2종 보통 (자동)"),
            ("P", "장롱 면허"),
        )
        PLAN_TYPES = (
            (None, "미선택"),
            ("T", "시간제"),
            ("G", "합격보장제"),
            ("P", "장롱 면허"),
        )
        model = User
        fields = (
            "username",
            "name",
            "birthday",
            "gender",
            "phone",
            "license_type",
            "plan_type",
            "is_staff",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "birthday": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "gender": forms.RadioSelect(
                choices=GENDERS,
                attrs={
                    "type": "radio",
                    "class": "form-check-input",
                },
            ),
            "phone": forms.TextInput(
                attrs={
                    "type": "tel",
                    "class": "form-control",
                },
            ),
            "license_type": forms.RadioSelect(
                choices=LICENSE_TYPES,
                attrs={
                    "type": "radio",
                    "class": "form-check-input",
                },
            ),
            "plan_type": forms.RadioSelect(
                choices=PLAN_TYPES,
                attrs={
                    "type": "radio",
                    "class": "form-check-input",
                },
            ),
            "is_staff": forms.RadioSelect(
                choices=[(True, "예"), (False, "아니오")],
                attrs={
                    "type": "radio",
                    "class": "form-check-input",
                },
            ),
        }
