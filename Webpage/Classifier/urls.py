from django.urls import path
from . import views


urlpatterns = [
    path('predict', views.predict_sentence, name='predict'),
    path('', views.index, name='index'),
]