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
        return reverse_lazy('voca:word_book_list') #마이페이지 링크 걸어주기


class SignOutView(generic.RedirectView):
    url = reverse_lazy('accounts:home')

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        auth_logout(request)
        return super(SignOutView, self).dispatch(request, *args, **kwargs)