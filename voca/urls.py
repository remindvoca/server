from django.urls import path, include
from voca.views import *

app_name='voca'

urlpatterns = [
    path('main/', mainview.as_view(), name='main'),
    path('upload/', uploadview.as_view(), name='upload'),
    path('upload/process/', process, name='process' ),
    path('upload/process/makeWord', makeWord, name='makeWord' ),
    #path('', views.main, name='main'),

    path('word_books/', WordBookListView.as_view(), name='word_book_list'),
    path('word_books/<int:word_book_id>/', WordDayListView.as_view(), name='word_day_list'),
    path('word_days/<int:word_day_id>/', WordListView.as_view(), name='word_list'),
]
