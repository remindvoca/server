from django.contrib import admin
from django.urls import path
from voca.views import *

urlpatterns = [
    path(r'', index),
]
