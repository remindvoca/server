from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import PDFModel
from .forms import PDF_Form
from accounts.models import User
from django.views import generic

login_url='accounts/sign_in/'

class mainview(generic.TemplateView):
    template_name = 'main.html'

#def main(request):
#    return render(request, 'pages/main.html',{})


# @login_required(login_url=login_url)
def upload(request):

    return render(request, 'pages/upload.html',{
        'form':PDF_Form()
    })

@login_required(login_url=login_url)
def process(request):
    if request.method == "POST":
        print(request.POST)
        form = PDF_Form(request.POST, request.FILES)
        # if form.is_valid():
        user_instance = User.objects.filter(username=request.user.username).get()
        # print(type(user_instance))
        # print(request.user.username)

        new_request=PDFModel.objects.create(
            filePath=request.FILES['file'],
            Account_userID=user_instance,
        )
        print('PDF uploaded.')

        return render(request, 'alert.html', {'msg': "Upload was successfully finished. We will let you know if rendering is finished!"})
    # return render(request, 'alert.html', {'msg': "Invalid Form for Video object"})
    return render(request, 'alert.html', {'msg': "잘못된 접근입니다"})