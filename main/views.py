import calendar

from django.utils import timezone
from django.views.generic.base import TemplateView


# Create your views here.
class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "메인"
        context["page_title"] = "메인"
        context["year_calendar"] = calendar.LocaleHTMLCalendar(locale="ko_KR").formatmonth(timezone.now().year, timezone.now().month)
        context["weekdays"] = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일","토요일",]

        return context
