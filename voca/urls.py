from django.urls import path, include
from voca.views import *

app_name='voca'

urlpatterns = [
    path('main/', mainview.as_view(), name='main'),
    #path('', views.main, name='main'),
]
