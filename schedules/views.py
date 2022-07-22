from django.views.generic.base import TemplateView
from django.apps import apps

# Create your views here.
class IndexView(TemplateView):
    template_name = "schedules/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app_name"] = apps.get_app_config(__package__).verbose_name
        
        return context