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

from schedules import views

app_name = apps.get_app_config(__package__).name

urlpatterns = [
    path("", views.ScheduleListView.as_view(), name="list"),
    path("<int:branch>/", views.BranchScheduleListView.as_view(), name="branch_list"),
    # path(
    #     "<int:branch>/<int:year>/",
    #     views.DateScheduleListView.as_view(),
    #     name="branch_year_schedule",
    # ),
    # path(
    #     "<int:branch>/<int:year>/<int:month>/",
    #     views.DateScheduleListView.as_view(),
    #     name="branch_month_schedule",
    # ),
    path(
        "<int:branch>/<int:year>/<int:week>/",
        views.WeekScheduleListView.as_view(),
        name="branch_week_schedule",
    ),
    # path(
    #     "<int:branch>/<int:year>/<int:month>/<int:day>/",
    #     views.DateScheduleListView.as_view(),
    #     name="branch_day_schedule",
    # ),
    path("add/", views.ScheduleCreateView.as_view(), name="add"),
]
