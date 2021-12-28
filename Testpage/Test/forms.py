from django import forms


class UploadFileForm(forms.Form):
    title = forms.ImageField()


class TextForm(forms.Form): #TODO: Make sure its working correctly
    text = forms.CharField(max_length=25)


class UploadTextForm(forms.Form):
    pass

# TODO: Use UploadFileForm as template but allow for a string (or document)
