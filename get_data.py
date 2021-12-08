import nltk
from xml.dom import minidom
import numpy as np
import tensorflow as tf
from tensorflow import keras


def get_data(filename):
    data = []
    labels = []
    dom = minidom.parse(filename)
    for qtag in dom.getElementsByTagName("utterance"):
        data.append(qtag.getAttribute('text'))
        if qtag.getAttribute("sensical") == "true":
            labels.append(1)
        else:
            labels.append(0)

    return data, labels


a, b = get_data('train_tested.xml')
a_array = np.asarray(a)
b_array = np.asarray(b)

tokenizer = keras.preprocessing.text.Tokenizer(num_words=100, oov_token='<OOv>')
tokenizer.fit_on_texts(a)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(a)

train_data = keras.preprocessing.sequence.pad_sequences(sequences, value=0, padding='post',maxlen=5)
