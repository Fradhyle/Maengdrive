from django.apps import apps
from django.db.models.fields.reverse_related import ManyToOneRel
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from schedules.forms import ScheduleForm
from schedules.models import Schedule
from users.models import User


# Create your views here.
class IndexView(TemplateView):
    template_name = "schedules/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = apps.get_app_config(__package__).verbose_name

        return context


class ScheduleListView(ListView):
    model = Schedule
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
        context["page_title"] = "일정 목록"
        context["verbose_names"] = self.get_verbose_names()

        return context


class ScheduleCreateView(CreateView):
    model = Schedule
    form_class = ScheduleForm
    success_url = reverse_lazy("schedules:list")

    def get_form_kwargs(self):
        kwargs = super(ScheduleCreateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "일정 추가"
        if self.request.user.is_superuser:
            context["user_list"] = User.objects.all()
        else:
            context["user_list"] = User.objects.filter(branch=self.request.user.branch)

        return context
