import tensorflow as tf
import numpy as np
from tensorflow import keras


def predict(random_sentence_list): #TODO: Make sure it is working


    model = keras.models.load_model('NLU_model')

    tokenizer = keras.preprocessing.text.Tokenizer(num_words=10000, oov_token='<OOV>') #TODO: Get real tokenizer from main
    train_data = ['this', 'is', 'a', 'temporary', 'text', 'for', 'making', 'a', 'tokenizer']
    tokenizer.fit_on_texts(train_data)
    word_index = tokenizer.word_index


    my_array = np.asarray(random_sentence_list)
    my_sequence = tokenizer.texts_to_sequences(my_array)
    padded_sequence = keras.preprocessing.sequence.pad_sequences(my_sequence, value=0, padding='post', maxlen=25)
    prediction = model.predict(padded_sequence)
    #TODO: Need to add decode_prediciton()??
    return prediction

if __name__ == '__main__': #TODO: Remove after this is working as intenden
    my_sentence = ["test test test test testing if this is still working or if it is not working as it is intedend"]
    result = predict(my_sentence)
    print(result)
