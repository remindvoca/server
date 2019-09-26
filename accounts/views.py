from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import never_cache
from django.shortcuts import render

from accounts.forms import UserCreationForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import LoginView

from voca.models import *

# todo: 임시 홈뷰
class HomeView(generic.TemplateView):
    template_name = 'home.html'


class BeforeSignUpView(generic.TemplateView):
    template_name = 'before_sign_up.html'


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'sign_up.html'
    success_url = reverse_lazy('accounts:sign_in')


class SignInView(LoginView):
    template_name = 'sign_in.html'

    def get_success_url(self):
        return reverse_lazy('voca:main') #마이페이지 링크 걸어주기


class SignOutView(generic.RedirectView):
    url = reverse_lazy('accounts:home')

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        auth_logout(request)
        return super(SignOutView, self).dispatch(request, *args, **kwargs)

class MyPageView(generic.ListView):
    model = FolderModel
    template_name = 'mypage.html'
    context_object_name = 'folders'

    def get_queryset(self):  # 컨텍스트 오버라이딩
        # return FolderModel.objects.filter(Account_userID=self.request.user)
        return ['TOEIC','TOEFL','수능','TOEIC_2','TOEFL_2',]

class VocaBookView(generic.ListView):
    model = VocaBookModel
    template_name = 'myVocaBooks.html'
    context_object_name = 'vocabooks'

    def get_queryset(self):  # 컨텍스트 오버라이딩
        # return FolderModel.objects.filter(Account_userID=self.request.user)
        return {
            'Intermediate': 20,
            'Regular': 30,
            'Actual': 25,
        }

class DailyBookView(generic.ListView):
    model = DailyBookModel
    template_name = 'daily.html'
    context_object_name = 'dailyBooks'

    def get_queryset(self):  # 컨텍스트 오버라이딩
        # return FolderModel.objects.filter(Account_userID=self.request.user)
        return list(range(1,21))