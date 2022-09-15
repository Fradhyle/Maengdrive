import datetime

from django.conf import settings
from django.db.models.fields.reverse_related import ManyToOneRel
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from branches.forms import BranchForm, HourForm, TimetableForm
from branches.models import Branch, Hour, Timetable


# Create your views here.
# Simple functions to handle few things.
def branch_shutdown(request, **kwargs):
    branch = Branch.objects.get(srl=kwargs["srl"])

    branch.closure = True

    branch.save()

    return HttpResponseRedirect(
        reverse_lazy("branches:detail", kwargs={"srl": branch.srl})
    )


def branch_open(request, **kwargs):
    branch = Branch.objects.get(srl=kwargs["srl"])

    branch.closure = False

    branch.save()

    return HttpResponseRedirect(
        reverse_lazy("branches:detail", kwargs={"srl": branch.srl})
    )


def init_timetable(request, **kwargs):
    # Get branch parameter from URL
    branch = Branch.objects.get(srl=kwargs["branch"])
    # Get and set is_holiday parameter from URL
    if kwargs["is_holiday"] == "False":
        is_holiday = False
    elif kwargs["is_holiday"] == "True":
        is_holiday = True
    hours = Hour.objects.get(branch=branch, is_holiday=is_holiday)
    converted_close_time = datetime.datetime.combine(
        datetime.datetime.now().date(), hours.close_time
    )
    class_time = datetime.timedelta(minutes=110)
    break_time = datetime.timedelta(minutes=10)
    current_time = datetime.datetime.combine(
        datetime.datetime.now().date(), hours.open_time
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

    return HttpResponseRedirect(reverse_lazy("branches:timetable_list"))


# Branch related Class Based Views
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
        context["page_title"] = f"{self.model._meta.verbose_name} 목록"
        context["verbose_names"] = self.get_verbose_names()

        return context


class BranchCreateView(CreateView):
    model = Branch
    form_class = BranchForm
    success_url = reverse_lazy("branches:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.model._meta.verbose_name} 추가"
        # !IMPORTANT: Please add juso.go.kr API Key if not using settings.json
        context["confmKey"] = settings.SETTINGS["confmKey"]

        return context


class BranchUpdateView(UpdateView):
    model = Branch
    form_class = BranchForm
    success_url = reverse_lazy("branches:list")

    def get_object(self, queryset=None):
        object = self.model.objects.get(srl=self.kwargs["srl"])
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.model._meta.verbose_name} 편집"
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

    def get_hours(self):
        return Hour.objects.filter(branch=self.kwargs["srl"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        context["hours"] = self.get_hours()
        context["verbose_names"] = self.get_verbose_names()
        context["page_title"] = f"{context['object'].name} 정보"

        return context


# Hour related Class Based Views
class HourListView(ListView):
    model = Hour
    paginate_by = 10

    def get_verbose_names(self):
        verbose_names = {}
        fields = self.model._meta.get_fields()
        for field in fields:
            if type(field) != ManyToOneRel and field.name not in [
                "is_holiday",
            ]:
                verbose_names[field.name] = field.verbose_name

        return verbose_names

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.model._meta.verbose_name} 목록"
        context["verbose_names"] = self.get_verbose_names()

        return context


class HourCreateView(CreateView):
    model = Hour
    form_class = HourForm
    success_url = reverse_lazy("Hours:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.model._meta.verbose_name} 추가"

        return context


class HourDetailView(DetailView):
    model = Hour

    def get_queryset(self):
        if "branch" in self.kwargs.keys():
            return self.model.objects.filter(branch=self.kwargs["branch"])
        else:
            return self.model.objects.all()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail"] = self.get_queryset()

        context["page_title"] = f"{context['detail'][0].branch} 시간표"

        return context


class HourUpdateView(UpdateView):
    model = Hour
    form_class = HourForm
    success_url = reverse_lazy("branches:list")

    def get_object(self, queryset=None):
        object = self.model.objects.get(srl=self.kwargs["srl"])

        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.model._meta.verbose_name} 편집"

        return context


# Timetable related Class Based Views
class TimetableListView(ListView):
    model = Timetable
    paginate_by = 10

    def get_verbose_names(self):
        verbose_names = {}
        fields = self.model._meta.get_fields()
        for field in fields:
            if type(field) != ManyToOneRel and field.name not in [
                "is_holiday",
            ]:
                verbose_names[field.name] = field.verbose_name

        return verbose_names

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.model._meta.verbose_name} 목록"
        context["verbose_names"] = self.get_verbose_names()

        return context


class TimetableCreateView(CreateView):
    model = Timetable
    form_class = TimetableForm
    success_url = reverse_lazy("timetables:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.model._meta.verbose_name} 추가"

        return context


class TimetableDetailView(DetailView):
    model = Timetable

    def get_queryset(self):
        if "branch" in self.kwargs.keys():
            return self.model.objects.filter(branch=self.kwargs["branch"])
        else:
            return self.model.objects.all()

    def get_object(self, queryset=None):
        if queryset:
            return queryset
        else:
            queryset = self.get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["detail"] = self.get_queryset()

        context["page_title"] = f"{context['detail'][0].branch} 시간표"

        return context


class TimetableUpdateView(UpdateView):
    model = Timetable
    form_class = TimetableForm
    success_url = reverse_lazy("branches:list")

    def get_object(self, queryset=None):
        object = self.model.objects.get(srl=self.kwargs["srl"])

        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.model._meta.verbose_name} 편집"

        return context
