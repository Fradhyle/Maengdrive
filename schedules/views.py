from django.apps import apps
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


class ScheduleDayView(ListView):
    pass


class AddScheduleView(CreateView):
    model = Schedule
    form_class = ScheduleForm
    success_url = reverse_lazy("schedules:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        context["page_title"] = "일정 추가"

        return context
