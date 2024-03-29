from unicodedata import name

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import Group
from django.db.models.fields.reverse_related import ManyToOneRel
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from users.forms import UserForm
from users.models import User


# Create your views here.
class IndexView(TemplateView):
    template_name = "users/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "이용자 관리"
        context["srl"] = self.kwargs.get("srl")

        return context


class UserListView(ListView):
    model = User
    paginate_by = 10

    # 로그인한 이용자 지점 가져오기
    # if self.request.user.is_authenticated: self.request.user.branch

    def get_verbose_names(self):
        verbose_names = {}
        pass_list = [
            "password",
            "last_login",
            "active",
        ]
        fields = self.model._meta.get_fields()
        for field in fields:
            if type(field) != ManyToOneRel and field.name not in pass_list:
                verbose_names[field.name] = field.verbose_name

        return verbose_names

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "이용자 목록"
        context["verbose_names"] = self.get_verbose_names()

        return context


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("users:list")

    def form_valid(self, form):
        if form.is_valid:
            self.object = form.save()
            member_group = Group.objects.get(name="회원")
            self.object.groups.set([member_group])
            return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(UserCreateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "이용자 추가"

        return context


# class LoginView(auth_views.LoginView):
#     authenticate()
#     login()
