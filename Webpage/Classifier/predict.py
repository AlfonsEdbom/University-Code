import tensorflow as tf
import numpy as np
from tensorflow import keras
import os


def predict(random_sentence):

    #Load model


    model = tf.keras.models.load_model(direct)

    #Preprocessing
    my_list = [random_sentence]

    #predict
    prediction = model.predict(my_list)
    return prediction

if __name__ == '__main__': #TODO: Remove when sure everything is working
    dirname =os.path.dirname(__file__)
    #learningdir = os.path.join(dirname, '../Learning')
    #direct = os.path.join(learningdir, 'NLU_RNN_model')

    print(dirname)
    #my_sentence = "is this working as intended"
    #result = predict(my_sentence)
    #print(result)
