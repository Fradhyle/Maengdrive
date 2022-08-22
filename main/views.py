import calendar

from django.conf import settings
from django.utils import timezone
from django.views.generic.base import TemplateResponseMixin, TemplateView

# Create your views here.
BASE_DIR = settings.BASE_DIR
SETTINGS = settings.SETTINGS


class IndexView(TemplateView, TemplateResponseMixin):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "메인"
        context["page_title"] = "메인"
        context["year_calendar"] = calendar.LocaleHTMLCalendar(
            locale="ko_KR"
        ).formatmonth(timezone.localtime().year, timezone.localtime().month)
        context["weekdays"] = [
            "일요일",
            "월요일",
            "화요일",
            "수요일",
            "목요일",
            "금요일",
            "토요일",
        ]
        try:
            context["results"] = kwargs["results"]
        except KeyError:
            pass

        return context
