import nltk
from xml.dom import minidom
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import xml.etree.ElementTree as ET


def data_from_xml(filename):
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
    # print(type(train_data), type(train_labels), type(test_data), type(test_labels))
    train_data = np.asarray(train_data)
    train_labels = np.asarray(train_labels)
    test_data = np.asarray(test_data)
    test_labels = np.array(test_labels)
    # print(type(train_data), type(train_labels), type(test_data), type(test_labels))

    # shuffles the test data
    indices = np.arange(test_data.shape[0])
    np.random.shuffle(indices)
    test_data = test_data[indices]
    test_labels = test_labels[indices]

    # shuffles the train data
    indices = np.arange(test_data.shape[0])
    np.random.shuffle(indices)
    train_data = test_data[indices]
    train_labels = test_labels[indices]

    # create word to int dict and reverse
    tokenizer = keras.preprocessing.text.Tokenizer(num_words=10000, oov_token='<OOV>')
    tokenizer.fit_on_texts(train_data)
    word_index = tokenizer.word_index

    train_sequences = tokenizer.texts_to_sequences(train_data)
    test_sequences = tokenizer.texts_to_sequences(test_data)

    print(len(word_index))  #Q: why is this 17384 and not 10000?
                            #A: word_index is computed the same way, despite what value we assign to num_words. But it will only use
                            #   the assigned value to num_words when doing texts_to_sequences

    print(word_index['<OOV>'])
    print(1 in test_sequences)  # Q: This is not here, a problem or not (referring to the <OOV>)?
                                # A: Not a problem, since we're basically using the same book with the same words

    padded_train_data = keras.preprocessing.sequence.pad_sequences(train_sequences, value=0, padding='post', maxlen=25)
    padded_test_data = keras.preprocessing.sequence.pad_sequences(test_sequences, value=0, padding='post', maxlen=25)

    # Dividing into train and validation data
    train_values = padded_train_data #[:(len(padded_train_data) // 2)]
    validation_values = padded_test_data[(len(padded_test_data) // 2):]

    train_sensical = train_labels #[:(len(train_labels) // 2)]
    validation_sensical = test_labels[(len(test_data) // 2):]

    padded_test_data = padded_test_data[:len(test_data)//2]
    test_labels = test_labels[:len(test_labels)//2]

    # Create model
    vocab_size = 10000
    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab_size, 16))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(16, activation=tf.nn.relu))
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

    model.summary()

    # compile model
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # Fit the model
    history = model.fit(train_values,
                        train_sensical,
                        epochs=50,
                        batch_size=512,
                        validation_data=(validation_values, validation_sensical),
                        verbose=1)

    results = model.evaluate(padded_test_data, test_labels)

    random_sentence = ["Our oral antiviral candidate, if authorized or approved, could have a meaningful impact on "
                       "the lives of many, as the data further support the efficacy of paxlovid in reducing "
                       "hospitalization and death and show a substantial decrease in viral load"]
    my_array = np.asarray(random_sentence)
    my_sequence = tokenizer.texts_to_sequences(my_array)
    padded_sequence = keras.preprocessing.sequence.pad_sequences(my_sequence, value=0, padding='post', maxlen=25)

    print(f"predict stuff: {model.predict(padded_sequence)}")

    model.save('NLU_model/')
    return results


if __name__ == "__main__":
    train_data, train_labels = data_from_xml('train_full.xml')
    # print(f'{train_data[-1]}, {train_labels[-1]}')
    test_data, test_labels = data_from_xml('test_full.xml')
    # print(f'{test_data[-1]}, {test_labels[-1]}')
    result = model_preprocessing(train_data, train_labels, test_data, test_labels)
    print(f"The result is {result}")

