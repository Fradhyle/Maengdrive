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

from business_hours import views

app_name = apps.get_app_config(__package__).name

urlpatterns = [
    path("", views.BusinessHoursListView.as_view(), name="list"),
    path("add/", views.BusinessHoursCreateView.as_view(), name="add"),
    path("<int:branch>", views.BusinessHoursDetailView.as_view(), name="detail"),
]