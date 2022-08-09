from django.apps import apps
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from schedules.forms import TimetableForm
from schedules.models import Schedule, Timetable


# Create your views here.
class IndexView(TemplateView):
    template_name = "schedules/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = apps.get_app_config(__package__).verbose_name

        return context


class AddTimetableView(CreateView):
    model = Timetable
    form_class = TimetableForm
    success_url = reverse_lazy("schedules:index")

    def form_valid(self, form):
        print(form.cleaned_data)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "시간표 추가"

        return context
