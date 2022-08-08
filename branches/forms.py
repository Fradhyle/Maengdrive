from django import forms
from django.core.validators import RegexValidator
from django.forms import CharField, ModelForm

from branches.models import Branch

phone_validator = RegexValidator(
    regex="\d{2,4}-?\d{3,4}(-?\d{4})?",
    message="올바른 전화번호 형식이 아닙니다.",
)


class BranchForm(ModelForm):
    def clean(self):
        self.cleaned_data = super().clean()
        self.cleaned_data["phone1"] = self.clean_phone1()
        self.cleaned_data["phone2"] = self.clean_phone2()

    def clean_phone1(self):
        phone = self.cleaned_data["phone1"]
        phone = phone.replace("-", "")

        if phone[0:2] == "02" and len(phone) == 9:
            phone = [phone[0:2], phone[2:5], phone[5:]]
            phone = "".join(phone)
        elif phone[0:2] == "02" and len(phone) == 10:
            phone = [phone[0:2], phone[2:6], phone[6:]]
            phone = "".join(phone)
        elif phone[0] != 0 and len(phone) == 8:
            phone = [phone[0:4], phone[4:]]
            phone = "".join(phone)
        elif len(phone) == 10:
            phone = [phone[0:3], phone[3:6], phone[6:]]
            phone = "".join(phone)
        elif len(phone) == 11:
            phone = [phone[0:3], phone[3:7], phone[7:]]
            phone = "".join(phone)

        return phone

    def clean_phone2(self):
        phone = self.cleaned_data["phone2"]
        phone = phone.replace("-", "")

        if phone[0:2] == "02" and len(phone) == 9:
            phone = [phone[0:2], phone[2:5], phone[5:]]
            phone = "".join(phone)
        elif phone[0:2] == "02" and len(phone) == 10:
            phone = [phone[0:2], phone[2:6], phone[6:]]
            phone = "".join(phone)
        elif len(phone) == 8:
            phone = [phone[0:4], phone[4:]]
            phone = "".join(phone)
        elif len(phone) == 10:
            phone = [phone[0:3], phone[3:6], phone[6:]]
            phone = "".join(phone)
        elif len(phone) == 11:
            phone = [phone[0:3], phone[3:7], phone[7:]]
            phone = "".join(phone)

        return phone

    class Meta:
        model = Branch
        fields = [
            "name",
            "postcode",
            "address1",
            "address2",
            "phone1",
            "phone2",
        ]
        labels = {
            "name": "지점명",
            "postcode": "우편번호",
            "address1": "도로명 주소",
            "address2": "상세 주소",
            "phone1": "전화번호 1",
            "phone2": "전화번호 2",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "'점'을 포함한 지점명을 입력하세요.",
                }
            ),
            "postcode": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "주소 검색을 이용하세요.",
                    "readonly": "",
                    "aria-describedby": "id_postcode",
                }
            ),
            "address1": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "주소 검색을 이용하세요.",
                    "readonly": "",
                    "aria-describedby": "id_address1",
                }
            ),
            "address2": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "상세 주소를 입력하세요.",
                    "aria-describedby": "id_address2",
                }
            ),
            "phone1": forms.TextInput(
                attrs={
                    "type": "tel",
                    "class": "form-control",
                    "placeholder": "전화번호를 입력하세요.",
                }
            ),
            "phone2": forms.TextInput(
                attrs={
                    "type": "tel",
                    "class": "form-control",
                    "placeholder": "전화번호를 입력하세요.",
                }
            ),
        }
