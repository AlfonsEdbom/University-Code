import nltk
from xml.dom import minidom
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import xml.etree.ElementTree as ET




def get_data(filename):
    text = []
    labels = []
    dom = minidom.parse(filename)
    for qtag in dom.getElementsByTagName("utterance"):
        text.append(qtag.getAttribute('text'))
        if qtag.getAttribute("sensical") == "true":
            labels.append(1)
        else:
            labels.append(0)

    return text, labels


def model_preprocessing(train_data, train_labels, test_data, test_labels):
    #For some reason, these does not convert to numpy array when using np.array
    #print(type(train_data), type(train_labels), type(test_data), type(test_labels))
    train_data = np.asarray(train_data)
    train_labels = np.asarray(train_labels)
    test_data = np.asarray(test_data)
    test_labels = np.array(test_labels)
    #print(type(train_data), type(train_labels), type(test_data), type(test_labels))

    #create word to int dict and reverse
    tokenizer = keras.preprocessing.text.Tokenizer(num_words=10000, oov_token='<00v>') #00v or <UNK> does it matter?
    tokenizer.fit_on_texts(train_data)
    word_index = tokenizer.word_index
    train_sequences = tokenizer.texts_to_sequences(train_data)
    test_sequences = tokenizer.texts_to_sequences(test_data)

    print(len(word_index)) #why is this 12432 and not 10000?????
    print('<00v>' in test_sequences) #This is not here, a problem or not?

    print(train_sequences[0])
    padded_train_data = keras.preprocessing.sequence.pad_sequences(train_sequences, value=0, padding='post', maxlen=25)
    padded_test_data = keras.preprocessing.sequence.pad_sequences(test_sequences, value=0, padding='post', maxlen=25)
    print(padded_train_data[0])

    #Create model
    vocab_size = 10000
    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab_size, 16))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(16, activation=tf.nn.relu))
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

    model.summary()

    #compile model
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])


    #Dividing into train and validation data
    train_values = padded_train_data[:(len(padded_train_data) // 2)]
    validation_values = padded_train_data[(len(padded_train_data) // 2):]

    train_sensical = train_labels[:(len(train_labels) // 2)]
    validation_sensical = train_labels[(len(train_data) // 2):]

    #Fit the model
    history = model.fit(validation_values,
                        validation_sensical,
                        epochs=10,
                        batch_size=512,
                        validation_data=(train_values, train_sensical),
                        verbose=1)

    results = model.evaluate(padded_test_data, test_labels)

    #print(f'Results: {results}')

    return results






if __name__ == "__main__":
    train_data, train_labels = get_data('train_full.xml')
    # print(f'{train_data[-1]}, {train_labels[-1]}')
    test_data, test_labels = get_data('test_full.xml')
    # print(f'{test_data[-1]}, {test_labels[-1]}')
    result = model_preprocessing(train_data, train_labels, test_data, test_labels)
    print(f"The result is damdamdam: {result}")

