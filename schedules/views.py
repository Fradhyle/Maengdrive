import datetime

from django.apps import apps
from django.db.models.fields.reverse_related import ManyToOneRel
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from schedules.forms import ScheduleForm
from schedules.models import Schedule
from timetables.models import Timetable
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
            print(field)
            if type(field) != ManyToOneRel:
                verbose_names[field.name] = field.verbose_name

        return verbose_names

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "일정 목록"
        context["verbose_names"] = self.get_verbose_names()

        return context


class BranchScheduleListView(ListView):
    model = Schedule
    paginate_by = 10

    def get_verbose_names(self):
        verbose_names = {}
        fields = self.model._meta.get_fields()
        for field in fields:
            if type(field) != ManyToOneRel:
                verbose_names[field.name] = field.verbose_name

        return verbose_names

    def get_queryset(self):
        if "branch" in self.kwargs.keys():
            if "day" in self.kwargs.keys():
                return self.model.objects.filter(branch=self.kwargs["branch"])
            elif "week" in self.kwargs.keys():
                return self.model.objects.filter(branch=self.kwargs["branch"])
            elif "month" in self.kwargs.keys():
                return self.model.objects.filter(branch=self.kwargs["branch"])
            elif "year" in self.kwargs.keys():
                return self.model.objects.filter(branch=self.kwargs["branch"])
            else:
                return self.model.objects.filter(branch=self.kwargs["branch"])
        else:
            return self.model.objects.all()

    def get_object(self):
        return self.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "일정 목록"
        context["verbose_names"] = self.get_verbose_names()

        return context


class WeekScheduleListView(ListView):
    model = Schedule
    paginate_by = 10
    template_name = "schedules/branch_schedule_list_week.html"

    def get_dates_of_week(self):
        year = self.kwargs["year"]
        week = self.kwargs["week"]
        dates_of_week = []
        for day in range(1, 8):
            dates_of_week.append(datetime.datetime.fromisocalendar(year, week, day))

        return dates_of_week

    def get_verbose_names(self):
        verbose_names = {}
        fields = self.model._meta.get_fields()
        for field in fields:
            if type(field) != ManyToOneRel:
                verbose_names[field.name] = field.verbose_name

        return verbose_names

    def get_queryset(self):
        object_list = []
        date_list = self.get_dates_of_week()

        if all(e in self.kwargs.keys() for e in ["branch", "year", "week"]):
            queryset = self.model.objects.filter(
                branch=self.kwargs["branch"],
                date__year=self.kwargs["year"],
                date__week=self.kwargs["week"],
            )

            maximum_period = int(
                Timetable.objects.filter(branch=self.kwargs["branch"])
                .order_by("-period")[0]
                .period
            )

            for period in range(1, maximum_period + 1):
                schedule_list = [period]
                schedules = queryset.filter(period=period)
                for date in date_list:
                    day_schedules = schedules.filter(date=date)
                    if len(day_schedules) == 0:
                        schedule_list.append("")
                    else:
                        schedule_list.append(day_schedules)
                object_list.append(schedule_list)

            return object_list
        else:
            return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "일정 목록"
        context["branch"] = self.kwargs["branch"]
        context["year"] = self.kwargs["year"]
        context["week"] = self.kwargs["week"]
        context["dates_of_week"] = self.get_dates_of_week()
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
        if self.request.user.superuser:
            context["user_list"] = User.objects.all()
        else:
            context["user_list"] = User.objects.filter(branch=self.request.user.branch)

        return context
