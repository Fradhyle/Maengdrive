"""Maengdrive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.apps import apps
from django.urls import path

from branches import views

app_name = apps.get_app_config(__package__).name

urlpatterns = [
    path(
        "",
        views.BranchListView.as_view(),
        name="branch_list",
    ),
    path(
        "add/",
        views.BranchCreateView.as_view(),
        name="branch_add",
    ),
    path(
        "<int:srl>/",
        views.BranchDetailView.as_view(),
        name="branch_detail",
    ),
    path(
        "<int:srl>/update/",
        views.BranchUpdateView.as_view(),
        name="branch_update",
    ),
    path(
        "<int:srl>/open",
        views.branch_open,
        name="branch_open",
    ),
    path(
        "<int:srl>/shutdown",
        views.branch_shutdown,
        name="branch_shutdown",
    ),
    path(
        "h/",
        views.HourListView.as_view(),
        name="hour_list",
    ),
    path(
        "h/add/",
        views.HourCreateView.as_view(),
        name="hour_add",
    ),
    path(
        "h/<int:branch>/",
        views.TimetableDetailView.as_view(),
        name="hour_detail",
    ),
    path(
        "h/<int:srl>/update/",
        views.TimetableUpdateView.as_view(),
        name="hour_update",
    ),
    path(
        "t/",
        views.TimetableListView.as_view(),
        name="timetable_list",
    ),
    path(
        "t/add/",
        views.TimetableCreateView.as_view(),
        name="timetable_add",
    ),
    path(
        "t/<int:branch>/",
        views.TimetableDetailView.as_view(),
        name="timetable_detail",
    ),
    path(
        "t/<int:srl>/update/",
        views.TimetableUpdateView.as_view(),
        name="timetable_update",
    ),
    path(
        "t/<int:branch>/init/<str:is_holiday>",
        views.init_timetable,
        name="timetable_init",
    ),
]
