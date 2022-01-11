from django import forms


class UploadFileForm(forms.Form):
    title = forms.ImageField()


class TextForm(forms.Form):
    text = forms.CharField(label='text', max_length=200)

