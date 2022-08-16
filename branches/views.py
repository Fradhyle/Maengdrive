import datetime

from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.reverse_related import ManyToOneRel
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from branches.forms import BranchForm
from branches.models import Branch


# Create your views here.
class BranchListView(ListView):
    model = Branch
    paginate_by = 10

    def get_verbose_names(self):
        verbose_names = {}
        fields = self.model._meta.get_fields()
        for field in fields:
            if type(field) != ManyToOneRel:
                verbose_names[field.name] = field.verbose_name

        return verbose_names

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "지점 목록"
        context["verbose_names"] = self.get_verbose_names()

        return context


class AddBranchView(CreateView):
    model = Branch
    form_class = BranchForm
    success_url = reverse_lazy("branches:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "지점 추가"
        # !IMPORTANT: Please add juso.go.kr API Key if not using settings.json
        context["confmKey"] = settings.SETTINGS["confmKey"]

        return context


class BranchDetailView(DetailView):
    model = Branch

    def get_queryset(self):
        if "srl" in self.kwargs.keys():
            return self.model.objects.filter(srl=self.kwargs.get("srl"))
        else:
            return self.model.objects.all()

    def get_object(self, queryset=None):
        try:
            if len(queryset) == 1:
                return queryset.get()
            else:
                return self.model.objects.filter(srl=self.kwargs.get("srl"))
        except TypeError:
            return self.model.objects.filter(srl=self.kwargs.get("srl"))

    def clean_object(self, object):
        new_object = {}
        for key, value in object.__dict__.items():
            try:
                verbose_name = self.model._meta.get_field(key).verbose_name
            except FieldDoesNotExist:
                pass
            else:
                new_object[verbose_name] = value

        return new_object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        object = self.get_object(queryset)
        context["branch_detail"] = self.clean_object(object)
        context["page_title"] = context["branch_detail"]["지점명"] + "점 정보"

        return context
