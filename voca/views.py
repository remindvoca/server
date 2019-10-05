from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from django.conf import settings
import os
import shutil


from accounts.models import User
from .forms import PDF_Form
from .models import PDFModel, WordBook, WordDay, Word

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
        form = PDF_Form(request.POST, request.FILES)
        # if form.is_valid():
        user_instance = User.objects.filter(username=request.user.username).get()
        #print(type(user_instance))
        #print(user_instance)
        #print(request.user.username)

        '''
        #폴더 생성
        if not os.path.isdir(os.path.join(settings.MEDIA_ROOT,user_instance.username)):
            os.mkdir(os.path.join(settings.MEDIA_ROOT,user_instance.username))
        '''
        new_request=PDFModel.objects.create(
            filePath=request.FILES['file'],
            Account_userID=user_instance,
        )
        print(request.FILES)
        print('PDF uploaded.')

        return render(request, 'alert.html', {'msg': "Upload was successfully finished. We will let you know if rendering is finished!"})
    '''
    # 처음 파일올리는 폼 줄때
    else:
        user_name = request.session['user_name']
        request.session['path'] = os.path.join(str(user_name))

        # 처음 들어올 때 다 지움
        if os.path.isdir(os.path.join(settings.MEDIA_ROOT, user_name)):
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, user_name))

        print(request.session['path'])
        # 파일을 받을 준비를 하자
    '''
    # return render(request, 'alert.html', {'msg': "Invalid Form for Video object"})
    return render(request, 'alert.html', {'msg': "잘못된 접근입니다"})


class WordBookListView(generic.ListView):
    template_name = 'word_book_list.html'
    model = WordBook

    def get_queryset(self):
        queryset = super(WordBookListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class WordDayLIstView(generic.ListView):
    template_name = 'word_day_list.html'
    model = WordDay

    def get_queryset(self):
        queryset = super(WordDayLIstView, self).get_queryset()
        word_book = self.kwargs.get('word_book_Id')
        return queryset.filter(word_book=word_book)


class WordListView(generic.ListView):
    template_name = 'word_list.html'
    model = Word

    def get_queryset(self):
        queryset = super(WordListView, self).get_queryset()
        word_day = self.kwargs.get('word_day_id')
        return queryset.filter(word_day=word_day)


class WordDetailView(generic.DetailView):
    template_name = 'word_detail.html'
    pk_url_kwarg = 'word_id'
    model = Word
