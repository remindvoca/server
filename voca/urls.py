from django.urls import path, include
from . import views

app_name='voca'

urlpatterns = [
    path('', views.main, name='main'),
    path('upload/', views.upload, name='upload'),
    path('upload/process/', views.process, name='process'),
]
