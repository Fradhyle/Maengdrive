from django.conf import settings
from django.db.models.fields.reverse_related import ManyToOneRel
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from branches.forms import BranchForm
from branches.models import Branch


# Create your views here.
def branch_shutdown(request, **kwargs):
    branch = Branch.objects.get(srl=kwargs["srl"])

    branch.closure = True

    branch.save()

    return HttpResponseRedirect(
        reverse_lazy("branches:detail", kwargs={"srl": branch.srl})
    )


def branch_reopen(request, **kwargs):
    branch = Branch.objects.get(srl=kwargs["srl"])

    branch.closure = False

    branch.save()

    return HttpResponseRedirect(
        reverse_lazy("branches:detail", kwargs={"srl": branch.srl})
    )


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

    def get_verbose_names(self):
        verbose_names = {}
        fields = self.model._meta.get_fields()
        for field in fields:
            if type(field) != ManyToOneRel:
                verbose_names[field.name] = field.verbose_name

        return verbose_names

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = super().get_queryset()

        pk = self.kwargs["srl"]
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            print("No object found")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        context["verbose_names"] = self.get_verbose_names()
        context["page_title"] = f"{context['object'].name} 정보"

        return context
