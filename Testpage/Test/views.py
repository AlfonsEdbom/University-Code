from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from .forms import TextForm
from .models import PredictString
from .predict import predict

import tensorflow as tf
from tensorflow import keras
import numpy as np


def index(request):
    template = loader.get_template('index.html')

    return render(request, 'index.html')


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

def test(request):
    context = {}
    if request.method =='POST':
        form = TextForm(request.POST)
        if form.is_valid():
            t = form.cleaned_data["text"]
            context["text"] = t
            prediction = predict(t)
            context["prediction"] = prediction
    else:
        render(request, 'test.html')

    return render(request, 'test.html', context)

def predict_text(request):
    context = {}
    if request.method == "POST":
        form = TextForm(request.POST) #If a file is uploaded request.FILES is needed also
        #if form.is_valid():
            #text_string = form.cleaned_data["text"]
            #t = PredictString(text=text_string)
            #t.save()

            #result = predict(["This", "is", "a", "temporary", "prediction", "list"]) #TODO: Add the right string here
            #resp = {'data': "maybe t", 'result': result} #TODO: Figure out what should be here
            #return render(request, "Test/result.html", resp)
    else:
        pass

    return render(request, 'predict.html', context)
def predict_text_old(request):
    context = {}
    if request.method == "POST":
        form = TextForm(request.POST) #TODO: If a file is uploaded request.FILES is needed also
        if form.is_valid():
            text_string = form.cleaned_data["text"]
            t = PredictString(text=text_string)
            t.save()

            result = predict(["This", "is", "a", "temporary", "prediction", "list"]) #TODO: Add the right string here
            resp = {'data': "maybe t", 'result': result} #TODO: Figure out what should be here
            return render(request, "Test/result.html", resp)
    else:
        return render(request, "Test/predict.html")
