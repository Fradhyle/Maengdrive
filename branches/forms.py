import datetime

from django import forms
from django.forms import ModelChoiceField, ModelForm

from branches.models import Branch, Hour, Timetable


class BranchForm(ModelForm):
    def format_phone_number(self, field_name):
        phone_number = self.cleaned_data[field_name]
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

    def clean_phone1(self):
        return self.format_phone_number("phone1")

    def clean_phone2(self):
        return self.format_phone_number("phone2")

    def clean_lesson_time(self):
        time = self.data["lesson_time"]
        return datetime.timedelta(minutes=int(time))

    def clean_break_time(self):
        time = self.data["break_time"]
        return datetime.timedelta(minutes=int(time))

    def clean_name(self):
        name = self.cleaned_data["name"]
        if name.startswith(("개발", "테스트")) or name.endswith("점"):
            return name
        else:
            return name + "점"

    class Meta:
        model = Branch
        fields = (
            "name",
            "equipment_count",
            "postcode",
            "address1",
            "address2",
            "phone1",
            "phone2",
            "lesson_time",
            "break_time",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "지점명을 입력하세요.",
                    "autocomplete": "organization",
                }
            ),
            "equipment_count": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "장비 대수를 입력하세요.",
                }
            ),
            "postcode": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "주소 검색을 이용하세요.",
                    "readonly": "",
                    "aria-describedby": "id_postcode",
                    "autocomplete": "postal-code",
                }
            ),
            "address1": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "주소 검색을 이용하세요.",
                    "readonly": "",
                    "aria-describedby": "id_address1",
                    "autocomplete": "address-line1",
                }
            ),
            "address2": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "상세 주소를 입력하세요.",
                    "aria-describedby": "id_address2",
                    "autocomplete": "address-line2",
                }
            ),
            "phone1": forms.TextInput(
                attrs={
                    "type": "tel",
                    "class": "form-control",
                    "placeholder": "전화번호를 입력하세요.",
                    "autocomplete": "tel-national",
                }
            ),
            "phone2": forms.TextInput(
                attrs={
                    "type": "tel",
                    "class": "form-control",
                    "placeholder": "전화번호를 입력하세요.",
                    "autocomplete": "tel-national",
                }
            ),
            "lesson_time": forms.NumberInput(
                attrs={
                    "aria-describedby": "minute-unit",
                    "class": "form-control",
                }
            ),
            "break_time": forms.NumberInput(
                attrs={
                    "aria-describedby": "minute-unit",
                    "class": "form-control",
                }
            ),
        }


class HourForm(ModelForm):
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
        model = Hour
        fields = (
            "branch",
            "is_holiday",
            "open_time",
            "close_time",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "지점명을 입력하세요.",
                    "autocomplete": "organization",
                }
            ),
            "is_holiday": forms.NullBooleanSelect(
                attrs={
                    "class": "form-select",
                }
            ),
            "open_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                }
            ),
            "close_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                }
            ),
        }


class TimetableForm(ModelForm):
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
        model = Timetable
        fields = (
            "branch",
            "period",
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
            "is_holiday": forms.NullBooleanSelect(
                attrs={
                    "class": "form-select",
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
