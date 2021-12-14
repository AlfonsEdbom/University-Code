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

    print(test_data[0])
    print(test_labels[0])

    indices = np.arange(test_data.shape[0])
    np.random.shuffle(indices)
    test_data = test_data[indices]
    test_labels = test_labels[indices]

    print(test_data[0])
    print(test_labels[0])


    indices = np.arange(test_data.shape[0])
    np.random.shuffle(indices)
    train_data = test_data[indices]
    train_labels = test_labels[indices]

    #create word to int dict and reverse
    tokenizer = keras.preprocessing.text.Tokenizer(num_words=10000, oov_token='<00v>') #00v or <UNK> does it matter?
    tokenizer.fit_on_texts(train_data)
    word_index = tokenizer.word_index
    print(word_index)
    train_sequences = tokenizer.texts_to_sequences(train_data)
    test_sequences = tokenizer.texts_to_sequences(test_data)

    print(len(word_index)) #why is this 12432 and not 10000?????
    print('<00v>' in test_sequences) #This is not here, a problem or not?

    print(train_sequences[0])
    padded_train_data = keras.preprocessing.sequence.pad_sequences(train_sequences, value=0, padding='post', maxlen=25)
    padded_test_data = keras.preprocessing.sequence.pad_sequences(test_sequences, value=0, padding='post', maxlen=25)
    print(padded_train_data[0])

    #Dividing into train and validation data
    train_values = padded_train_data #[:(len(padded_train_data) // 2)]
    validation_values = padded_test_data[(len(padded_test_data) // 2):]

    train_sensical = train_labels #[:(len(train_labels) // 2)]
    validation_sensical = test_labels[(len(test_data) // 2):]

    padded_test_data = padded_test_data[:len(test_data)//2]
    test_labels = test_labels[:len(test_labels)//2]

    print("lengths")
    print(len(validation_values))
    print(len(validation_sensical))
    print(len(train_values))
    print(len(train_sensical))
    print(len(padded_test_data))
    print(len(test_labels))


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



    #Fit the model
    history = model.fit(train_values,
                        train_sensical,
                        epochs=50,
                        batch_size=512,
                        validation_data=(validation_values, validation_sensical),
                        verbose=1)

    results = model.evaluate(padded_test_data, test_labels)

    random_sentence = ["Our oral antiviral candidate, if authorized or approved, could have a meaningful impact on the lives of many, as the data further support the efficacy of paxlovid in reducing hospitalization and death and show a substantial decrease in viral load"]
    my_array = np.asarray(random_sentence)
    my_sequence = tokenizer.texts_to_sequences(my_array)
    padded_sequence = keras.preprocessing.sequence.pad_sequences(my_sequence, value=0, padding='post', maxlen=25)

    print(f"predict stuff: {model.predict(padded_sequence)}")



    #print(f'Results: {results}')

    return results







if __name__ == "__main__":
    train_data, train_labels = get_data('train_full.xml')
    # print(f'{train_data[-1]}, {train_labels[-1]}')
    test_data, test_labels = get_data('test_full.xml')
    # print(f'{test_data[-1]}, {test_labels[-1]}')
    result = model_preprocessing(train_data, train_labels, test_data, test_labels)
    print(f"The result is {result}")

