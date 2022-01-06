from xml.dom import minidom
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt


def plot_loss(model_data):
    history_dict = model_data.history

    acc = history_dict['accuracy']
    val_acc = history_dict['val_accuracy']
    loss = history_dict['loss']
    val_loss = history_dict['val_loss']
    epochs = range(1, len(acc) + 1)

    # "bo" is for "blue dot"
    plt.plot(epochs, loss, 'bo', label='Training loss')
    # b is for "solid blue line"
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()


def plot_accuracy(model_data):
    history_dict = model_data.history

    acc = history_dict['accuracy']
    val_acc = history_dict['val_accuracy']
    loss = history_dict['loss']
    val_loss = history_dict['val_loss']
    epochs = range(1, len(acc) + 1)

    # "bo" is for "blue dot"
    plt.plot(epochs, acc, 'bo', label='Training acc')
    # b is for "solid blue line"
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend(loc='lower right')

    plt.show()


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


def model_preprocessing(data, labels):

    # shuffle the data and labels
    np_data = np.asarray(data)
    np_labels = np.asarray(labels)
    indices = np.arange(np_data.shape[0])
    np.random.shuffle(indices)
    shuffled_data = np_data[indices]
    shuffled_labels = np_labels[indices]

    #separate data into train and test data/labels
    cutoff_mark = int(len(data) * 0.8)
    train_data = np.asarray(shuffled_data[:cutoff_mark])
    train_labels = np.asarray(shuffled_labels[:cutoff_mark])

    test_data = np.asarray(shuffled_data[cutoff_mark:])
    test_labels = np.array(shuffled_labels[cutoff_mark:])

    # create word to int dict and reverse
    tokenizer = keras.preprocessing.text.Tokenizer(num_words=15000, oov_token='<OOV>')
    tokenizer.fit_on_texts(train_data)
    word_index = tokenizer.word_index

    #make sents to sequence of ints
    train_sequences = tokenizer.texts_to_sequences(train_data)
    test_sequences = tokenizer.texts_to_sequences(test_data)

    #json string to export
    json_tokenizer = tokenizer.to_json()

    padded_train_data = keras.preprocessing.sequence.pad_sequences(train_sequences, value=0, padding='post', maxlen=25)
    padded_test_data = keras.preprocessing.sequence.pad_sequences(test_sequences, value=0, padding='post', maxlen=25)

    # Dividing into test and validation data
    validation_data = padded_train_data[(len(padded_train_data) // 2):]
    validation_labels = train_labels[(len(padded_train_data) // 2):]

    train_data = padded_train_data[:(len(padded_train_data) // 2)]  # [:(len(train_labels) // 2)]
    train_labels = train_labels[:(len(padded_train_data) // 2)]

    # Create model
    vocab_size = 15000
    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab_size, 25))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(25, activation=tf.nn.relu))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

    model.summary()

    # compile model
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # Fit the model
    history = model.fit(train_data,
                        train_labels,
                        epochs=25,
                        batch_size=512,
                        validation_data=(validation_data, validation_labels),
                        verbose=1)

    results = model.evaluate(padded_test_data, test_labels)

    #random_sentence = ["Our oral antiviral candidate, if authorized or approved, could have a meaningful impact on "
     #                  "the lives of many, as the data further support the efficacy of paxlovid in reducing "
      #                 "hospitalization and death and show a substantial decrease in viral load"]
    #my_array = np.asarray(random_sentence)
    #my_sequence = tokenizer.texts_to_sequences(my_array)
    #padded_sequence = keras.preprocessing.sequence.pad_sequences(my_sequence, value=0, padding='post', maxlen=25)

    #print(f"predict stuff: {model.predict(padded_sequence)}")

    # model.save('NLU_model/')
    return results, json_tokenizer, history


if __name__ == "__main__":
    data, labels = data_from_xml('web_full.xml')
    # print(f'{train_data[-1]}, {train_labels[-1]}')
    # test_data, test_labels = data_from_xml('test_full.xml')
    # print(f'{test_data[-1]}, {test_labels[-1]}')
    result, json_string, history = model_preprocessing(data, labels)
    print(f"The result is {result}")
    plot_loss(history)
    plot_accuracy(history)

    # with open('Testpage/Test/text_tokenizer.json', 'w') as f:
    #    f.write(json_string)

    # new_tokenizer = keras.preprocessing.text.tokenizer_from_json(json_string2)
