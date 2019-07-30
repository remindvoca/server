from django import forms
from .models import PDFModel

class PDF_Form(forms.ModelForm):
    class Meta:
        model = PDFModel
        fields = (
            'filePath',
            'Account_userID',
        )

        # widgets = {
        #     'Account_userID': forms.HiddenInput(),
        # }
