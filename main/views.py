import calendar
import json
import math

import requests
from django.utils import timezone
from django.views.generic.base import TemplateResponseMixin, TemplateView
from django.conf import settings

# Create your views here.
BASE_DIR = settings.BASE_DIR
SETTINGS = settings.SETTINGS

class IndexView(TemplateView, TemplateResponseMixin):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "메인"
        context["page_title"] = "메인"
        context["year_calendar"] = calendar.LocaleHTMLCalendar(locale="ko_KR").formatmonth(timezone.localtime().year, timezone.localtime().month)
        context["weekdays"] = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일","토요일",]
        try:
            context["results"] = kwargs["results"]
        except KeyError:
            pass

        return context
        
    def log_keeper(self, filename, content):
        log_header = "Timestamp\tKeyword\tTotal Count\tCurrent Page\tCount Per Page\tError Code\tError Message\n"
        content["Timestamp"] = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(filename, mode="r", encoding="utf-8") as f:
                log_file = f.readlines()
        except FileNotFoundError:
            with open(filename, mode="w", encoding="utf-8") as f:
                f.writelines(log_header)
        finally:
            with open(filename, mode="r", encoding="utf-8") as f:
                log_file = f.readlines()

        if len(log_file) == 0:
            with open(filename, mode="w", encoding="utf-8") as f:
                f.write(log_header)                
        elif len(log_file) != 0 and log_header not in log_file[0]:
            log_file.insert(0, log_header)
            with open(filename, mode="w", encoding="utf-8") as f:
                f.writelines(log_file)

        with open(filename, mode="a+", encoding="utf-8") as f:
            f.seek(0)
            new_log = content["Timestamp"] + "\t" + content["keyword"] + "\t" + content["totalCount"] + "\t" + content["currentPage"] + "\t" + content["countPerPage"] + "\t" + content["errorCode"] + "\t" + content["errorMessage"] + "\n"
            f.write(new_log)
        
        return

    def search_addr(self, keyword, currentPage=1, countPerPage=10, **kwargs):
        base_url = "https://www.juso.go.kr/addrlink/addrLinkApiJsonp.do"

        kwargs["confmKey"] = SETTINGS["confmKey"]
        kwargs["currentPage"] = currentPage
        kwargs["countPerPage"] = countPerPage
        kwargs["keyword"] = keyword
        kwargs["resultType"] = "json"

        url = base_url + "?"

        for key, value in kwargs.items():
            if url[-1] == "?":
                try:
                    url += f"{key}={value}"
                except TypeError:
                    url += f"{key}={str(value)}"
            else:
                try:
                    url += f"&{key}={value}"
                except TypeError:
                    url += f"{key}={str(value)}"

        r = requests.get(url)
        r = r.content.decode(r.encoding).strip("()")
        r = json.loads(r)
        results = r["results"]
        results["common"]["keyword"] = keyword

        self.log_keeper("search_address_log.tsv", results["common"])

        results["common"]["totalPage"] = math.ceil(int(results["common"]["totalCount"]) / int(results["common"]["countPerPage"]))

        return results

    def post(self, request, **kwargs):
        context = self.get_context_data()
        if request.method == "POST":
            keyword = request.POST["search_input"]
            context["results"] = self.search_addr(keyword)
        return super().render_to_response(context)
