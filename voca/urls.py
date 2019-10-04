from django.urls import path, include
from voca.views import *

app_name='voca'

urlpatterns = [
    path('main/', mainview.as_view(), name='main'),
    path('upload/', uploadview.as_view(), name='upload'),
    path('upload/process/', process, name='process' )
    #path('', views.main, name='main'),
]
