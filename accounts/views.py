from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import UserCreationForm


# class SignUp(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup/signup.html'


class BeforeSignUpView(generic.TemplateView):
    template_name = 'before_sign_up.html'


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'sign_up.html'

    def get(self, request, *args, **kwargs):
        super(SignUpView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        super(SignUpView, self).post(request, *args, **kwargs)


class SignInView(generic.FormView):
    template_name = 'before_sign_up.html'


class SignOutView(generic.RedirectView):
    pass
