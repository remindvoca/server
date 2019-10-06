import os
import shutil

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from accounts.models import User
from .forms import *
from .models import PDFModel, WordBook, WordDay, Word
from pdf.pdftovoca import preprocessing as prep

import glob
from collections import Counter
import pandas as pd
import plotnine
from plotnine import *

login_url = 'accounts/sign_in/'


class mainview(generic.TemplateView):
    template_name = 'main.html'


#def main(request):
#    return render(request, 'pages/main.html',{})


#@login_required(login_url=login_url)
class uploadview(generic.TemplateView):
    template_name = 'upload.html'
#    return render(request, 'pages/upload.html',{
#        'form':PDF_Form()
#    })

def write_pdf_file(user,pdf):
    with open(os.path.join(settings.MEDIA_ROOT,user, pdf.name), 'wb+') as destination:
            for chunk in pdf.chunks():
                destination.write(chunk)


@login_required(login_url=login_url)
def process(request):
    if request.method == "POST":
        print(request.POST)
        #form = PDF_Form(request.POST, request.FILES)
        # if form.is_valid():
        user_instance = User.objects.filter(username=request.user.username).get()
        #print(type(user_instance))
        #print(user_instance)
        #print(request.user.username)

        
        #폴더 생성
        if not os.path.isdir(os.path.join(settings.MEDIA_ROOT,user_instance.username)):
            os.mkdir(os.path.join(settings.MEDIA_ROOT,user_instance.username))
        write_pdf_file(user_instance.username, request.FILES['file'])

        # new_request=PDFModel.objects.create(
        #     filePath=request.FILES['file'],
        #     Account_userID=user_instance,
        # )

        print(request.FILES)
        print('PDF uploaded.')

        return render(request, 'alert.html', {'msg': "Upload was successfully finished. We will let you know if rendering is finished!"})

    # 처음 파일올리는 폼 줄때
    else:
        print(request.session['path'])
        user_name = request.session['user_name']
        request.session['path'] = os.path.join(str(user_name))

        # 처음 들어올 때 다 지움
        if os.path.isdir(os.path.join(settings.MEDIA_ROOT, user_name)):
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, user_name))

        # 파일을 받을 준비를 하자

    # return render(request, 'alert.html', {'msg': "Invalid Form for Video object"})
    return render(request, 'alert.html', {'msg': "잘못된 접근입니다"})

@login_required(login_url=login_url)
def makeWord(request):
    user_name = request.user.username
    file_folder = os.path.join(settings.MEDIA_ROOT, user_name)
    # 폴더가 있으면 단어 분석을 시작한다.
    if os.path.isdir(file_folder):
        print(file_folder)
        # 모든 파일을 가져옴
        pdf_path = glob.glob(file_folder + "/*.pdf")
        txt_path = glob.glob(file_folder + "/*.txt")

        path_list = pdf_path + txt_path

        result = Counter('')

        # 예문을 만들기 위한 path
        text_path = []

        print(path_list)
        for path in path_list:
            if path[-3:] == 'pdf':
                pdf = prep(input_path=path)
                output_path = pdf.pdf2txt()
                text_path.append(output_path)

                pdf.clean_text()
                cnt = pdf.word_Frequency()

            elif path[-3:] == 'txt':
                txt = prep(output_path=path)
                text_path.append(path)

                txt.clean_text()
                cnt = txt.word_Frequency()

            result += cnt
            #여기서 디비 등록
            print(cnt)

            #visualization("visualization", file_folder, result)

    return render(request, 'main.html', {})


class WordBookListView(generic.ListView):
    template_name = 'word_book_list.html'
    model = WordBook

    def get_queryset(self):
        queryset = super(WordBookListView, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WordBookListView, self).get_context_data(object_list=object_list, **kwargs)
        context['remembered_word_count'] = self.request.user.words.filter(is_remembered=True).count()
        return context


class WordDayListView(generic.ListView):
    template_name = 'word_day_list.html'
    model = WordDay

    def setup(self, request, *args, **kwargs):
        super(WordDayListView, self).setup(request, *args, **kwargs)
        self.word_book = get_object_or_404(WordBook, id=self.kwargs.get('word_book_id'))
        self.word_book.updated_time = timezone.now()
        self.word_book.save(update_fields=['updated_time'])

    def get_queryset(self):
        queryset = super(WordDayListView, self).get_queryset()
        word_book = self.kwargs.get('word_book_id')
        return queryset.filter(word_book=word_book)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WordDayListView, self).get_context_data(object_list=None, **kwargs)
        context['word_book'] = self.word_book
        return context


class WordListView(generic.ListView):
    template_name = 'word_list.html'
    model = Word
    paginate_by = 1

    def setup(self, request, *args, **kwargs):
        super(WordListView, self).setup(request, *args, **kwargs)
        self.word_day = get_object_or_404(WordDay, id=self.kwargs.get('word_day_id'))
        self.word_day.checked_time = timezone.now()
        self.word_day.save(update_fields=['checked_time'])

    def get_queryset(self):
        queryset = super(WordListView, self).get_queryset()
        queryset = queryset.filter(word_day=self.word_day)
        queryset.update(is_remembered=True)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WordListView, self).get_context_data(object_list=None, **kwargs)
        context['word_day'] = self.word_day
        return context

class PDFupload(generic.CreateView):
    template_name = 'upload/process'
    form_class = WordbookCreateForm
    success_url = reverse_lazy('account:home')

    def get_form_kwargs(self):
        kwargs = super(PDFupload, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
