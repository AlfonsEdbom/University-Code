from django.shortcuts import render
from django.template import loader
from django.core.files.storage import FileSystemStorage
from .forms import TextForm
from .predict import predict

# Create your views here.
def index(request):
    template = loader.get_template('index.html')

    return render(request, 'index.html')


def predict_sentence(request):
    context = {}
    if request.method == 'POST':
        form = TextForm(request.POST)  # If a file is uploaded request.FILES is needed also
        if form.is_valid():
            t = form.cleaned_data["text"]
            context["text"] = t
            prediction = predict(t)
            context["prediction"] = prediction
    else:
        render(request, 'predict.html')

    return render(request, 'predict.html', context)


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)
