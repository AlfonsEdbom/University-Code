from django.shortcuts import render
from django.template import loader
from django.core.files.storage import FileSystemStorage
from .forms import TextForm
#from .predict import predict
import os
import tensorflow as tf

global my_model

model_dir = 'RNN_model'
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, model_dir)

my_model = tf.keras.models.load_model(model_path)

# Create your views here.
def index(request):
    template = loader.get_template('index.html')

    return render(request, 'index.html')


def predict_sentence(request):
    global my_model
    context = {}
    if request.method == 'POST':
        form = TextForm(request.POST)  # If a file is uploaded request.FILES is needed also
        if form.is_valid():
            t = form.cleaned_data["text"]
            context["text"] = t
            text_list = [t]
            prediction = my_model.predict(text_list)
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


if __name__ == '__main__':

    print(model_path)