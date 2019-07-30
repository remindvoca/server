from django.urls import path
from accounts.views import BeforeSignUpView, SignUpView


app_name = 'accounts'

urlpatterns = [
    path('before_sign_up/', BeforeSignUpView.as_view(), name='before_sign_up'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
]
