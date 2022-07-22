from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from branches.forms import BranchForm
from branches.models import Branch


# Create your views here.
class IndexView(TemplateView):
    template_name = "branches/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "지점"
        context["passed_list"] = range(5)
        context["page_title"] = "지점 목록"
        context["branches"] = Branch.objects.all().values()
        field_names = []
        fields = Branch._meta.get_fields()
        for e in fields:
            try:
                field_names.append(e.verbose_name)
            except AttributeError:
                pass
        context["field_names"] = field_names
        return context


class AddBranchView(CreateView):
    template_name = "branches/branch_form.html"
    form_class = BranchForm
    success_url = "/"

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "지점 추가"
        context["confmKey"] = settings.SETTINGS["confmKey"]

        return context


class BranchDetailView(DetailView):
    def get_queryset(self, srl):
        return Branch.objects.filter(srl=srl)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["branch_detail"] = self.get_queryset(self.kwargs["srl"])

        return context