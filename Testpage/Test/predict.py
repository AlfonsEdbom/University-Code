import tensorflow as tf
import numpy as np
from tensorflow import keras
import os


def predict(random_sentence):

    #Load model
    DIRNAME = os.path.dirname(__file__)
    model_dir = os.path.join(DIRNAME, 'NLU_model')
    model = keras.models.load_model(model_dir)

    #Load tokenizer
    tokenizer_path = os.path.join(DIRNAME, 'text_tokenizer.json')
    with open(tokenizer_path, 'r') as f:
        json_string = f.read()

    tokenizer = keras.preprocessing.text.tokenizer_from_json(json_string)

    #Preprocessing
    my_list = [random_sentence]
    my_array = np.asarray(my_list)
    my_sequence = tokenizer.texts_to_sequences(my_array)
    padded_sequence = keras.preprocessing.sequence.pad_sequences(my_sequence, value=0, padding='post', maxlen=25)

    #predict
    prediction = model.predict(padded_sequence)
    return prediction

if __name__ == '__main__': #TODO: Remove when sure everything is working
    my_sentence = "test test test test testing if this is still working or if it is not working as it is intedend"
    result = predict(my_sentence)
    print(result)
