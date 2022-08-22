import datetime

from django.db.models.fields.reverse_related import ManyToOneRel
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from branches.models import Branch
from business_hours.models import BusinessHours
from timetables.forms import TimetableForm
from timetables.models import Timetable


# Create your views here.
def init_timetable(request, **kwargs):
    branch = Branch.objects.get(srl=kwargs["branch"])
    if kwargs["is_holiday"] == "False":
        is_holiday = False
    elif kwargs["is_holiday"] == "True":
        is_holiday = True
    business_hours = BusinessHours.objects.get(branch=branch, is_holiday=is_holiday)
    converted_close_time = datetime.datetime.combine(
        datetime.datetime.now().date(), business_hours.close_time
    )
    class_time = datetime.timedelta(minutes=110)
    break_time = datetime.timedelta(minutes=10)
    current_time = datetime.datetime.combine(
        datetime.datetime.now().date(), business_hours.open_time
    )

    Timetable.objects.filter(branch=branch, is_holiday=is_holiday).delete()
    period_count = 1

    while current_time < converted_close_time:
        try:
            start_time = datetime.time(
                current_time.time().hour, current_time.time().minute
            )
            end_time = current_time + class_time
            end_time = datetime.time(end_time.time().hour, end_time.time().minute)
            t = Timetable(
                branch=branch,
                is_holiday=is_holiday,
                period=period_count,
                start_time=start_time,
                end_time=end_time,
            )
            t.save()
            current_time = current_time + class_time + break_time
            period_count += 1
        except IntegrityError:
            print("Error")

    return HttpResponseRedirect(reverse_lazy("timetables:list"))


class TimetableListView(ListView):
    model = Timetable
    paginate_by = 10

    def get_verbose_names(self):
        verbose_names = {}
        fields = self.model._meta.get_fields()
        for field in fields:
            if type(field) != ManyToOneRel and field.name not in ["srl", "is_holiday"]:
                verbose_names[field.name] = field.verbose_name

        return verbose_names

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "시간표 목록"
        context["verbose_names"] = self.get_verbose_names()

        return context


class TimetableCreateView(CreateView):
    model = Timetable
    form_class = TimetableForm
    success_url = reverse_lazy("timetables:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "시간표 추가"

        return context


class TimetableDetailView(DetailView):
    model = Timetable

    def get_queryset(self):
        if "branch" in self.kwargs.keys():
            return self.model.objects.filter(branch=self.kwargs["branch"])
        else:
            return self.model.objects.all()

    def get_object(self):
        return self.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail"] = self.get_queryset()

        context["page_title"] = f"{context['detail'][0].branch} 시간표"

        return context
