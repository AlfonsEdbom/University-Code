from django.shortcuts import render
from .forms import TextForm
import os
import tensorflow as tf

global my_model

model_dir = 'RNN_model'
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, model_dir)

my_model = tf.keras.models.load_model(model_path)


# Create your views here.
def index(request):
    return render(request, 'index.html')


def predict_sentence(request):
    global my_model
    context = {}
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            t = form.cleaned_data["text"]
            context["text"] = t
            text_list = [t]
            prediction = my_model.predict(text_list)
            context["prediction"] = prediction
    else:
        render(request, 'predict.html')

    return render(request, 'predict.html', context)
