from django import forms
from .models import WordBook

# class PDFForm(forms.ModelForm):
#     class Meta:
#         model = PDFModel
#         fields = (
#             'filePath',
#             'wordbook',
#         )
#
#     def __init__(self, *args, ):
#         super().__init__()
#


class WordbookCreateForm(forms.ModelForm):
    class Meta:
        model = WordBook
        fields = (
            'title',
        )

    def __init__(self, request ,*args, **kwargs):
        super(WordbookCreateForm, self).__init__(*args, **kwargs)
        self.fields['pdffile'] = forms.ModelChoiceField(queryset=WordBook.objects.pdf)
        self.user = request

    def save(self, commit=True):
        super(WordbookCreateForm, self).save(commit=True)
