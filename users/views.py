from django.db.models.fields.reverse_related import ManyToOneRel
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from users.models import User


# Create your views here.
class IndexView(TemplateView):
    template_name = "users/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "이용자 관리"
        context["srl"] = self.kwargs.get("srl")

        return context


class UserListView(ListView):
    model = User
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
        context["page_title"] = "이용자 목록"
        context["verbose_names"] = self.get_verbose_names()

        return context
