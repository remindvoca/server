import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic

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
