from django.apps import apps
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from timetables.forms import TimetableForm
from timetables.models import Timetable


# Create your views here.
class TimetableListView(ListView):
    model = Timetable
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "시간표 목록"
        context["timetables"] = Timetable.objects.all().values()
        field_names = []
        fields = Timetable._meta.get_fields()
        for field in fields:
            if field.name == "branch_srl":
                field_names.append("지점")
            else:
                try:
                    field_names.append(field.verbose_name)
                except AttributeError:
                    pass
        context["field_names"] = field_names

        return context


class AddTimetableView(CreateView):
    model = Timetable
    form_class = TimetableForm
    success_url = reverse_lazy("timetables:list")

    def form_valid(self, form):
        print(form.cleaned_data)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "시간표 추가"

        return context
