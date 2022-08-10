from django.apps import apps
from django.views.generic.base import TemplateView


# Create your views here.
class IndexView(TemplateView):
    template_name = "schedules/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = apps.get_app_config(__package__).verbose_name

        return context
