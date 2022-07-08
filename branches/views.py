from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

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


class AddBranchView(FormView):
    template_name = "branches/branch_form.html"
    form_class = BranchForm
    success_url = "/"

    def form_valid(self, form):
        return super().form_valid(form)