from django import forms

from branches.models import Branch


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ["name", "address", "phone1", "phone2",]
        labels = {
            "name": "지점명",
            "address": "주소",
            "phone1": "전화번호 1",
            "phone2": "전화번호 2",
        }

    def __str__(self):
        return self.name
