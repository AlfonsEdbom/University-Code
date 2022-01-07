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
    # make data into np arrays
    np_data = np.asarray(data)
    np_labels = np.asarray(labels)

    # shuffle labels and data
    indices = np.arange(np_data.shape[0])
    np.random.shuffle(indices)
    shuffled_data = np_data[indices]
    shuffled_labels = np_labels[indices]

    # separate data into train/test/validation data/labels
    train_cutoff = int(len(data) * 0.8)  # how much
    test_cutoff = int(len(data) * 0.9)

    train_data = np.asarray(shuffled_data[0: train_cutoff])  # from 0 to train_cutoff
    train_labels = np.asarray(shuffled_labels[0: train_cutoff])

    test_data = np.asarray(shuffled_data[train_cutoff: test_cutoff])  # from train_cutoff to test_cutoff
    test_labels = np.asarray(shuffled_labels[train_cutoff: test_cutoff])

    validation_data = np.asarray(shuffled_data[test_cutoff: -1])  # from test_cutoff to end
    validation_labels = np.asarray(shuffled_labels[test_cutoff: -1])

    # create word to int dict and reverse
    tokenizer = keras.preprocessing.text.Tokenizer(num_words=10000, oov_token='<OOV>')
    tokenizer.fit_on_texts(train_data)
    word_index = tokenizer.word_index
    json_tokenizer = tokenizer.to_json()  # needed to export tokenizer

    # converts str to int
    train_sequences = tokenizer.texts_to_sequences(train_data)
    test_sequences = tokenizer.texts_to_sequences(test_data)
    validation_sequences = tokenizer.texts_to_sequences(validation_data)

    # pad to same length
    sent_len = 25
    padded_train_data = keras.preprocessing.sequence.pad_sequences(train_sequences, value=0, padding='post',
                                                                   maxlen=sent_len)
    padded_test_data = keras.preprocessing.sequence.pad_sequences(test_sequences, value=0, padding='post',
                                                                  maxlen=sent_len)
    padded_validation_data = keras.preprocessing.sequence.pad_sequences(validation_sequences, value=0, padding='post',
                                                                        maxlen=sent_len)

    return padded_train_data, train_labels, padded_test_data, test_labels, padded_validation_data, validation_labels


def create_model(train_data, train_labels, test_data, test_labels, validation_data, validation_labels):
    vocab_size = 10000
    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab_size, 25))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(25, activation=tf.nn.relu))
    model.add(keras.layers.Dropout(0.5))
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

    results = model.evaluate(test_data, test_labels)

    #model.save('NLU_model/') #needed to export model

    # random_sentence = ["Our oral antiviral candidate, if authorized or approved, could have a meaningful impact on "
    #                  "the lives of many, as the data further support the efficacy of paxlovid in reducing "
    #                 "hospitalization and death and show a substantial decrease in viral load"]
    # my_array = np.asarray(random_sentence)
    # my_sequence = tokenizer.texts_to_sequences(my_array)
    # padded_sequence = keras.preprocessing.sequence.pad_sequences(my_sequence, value=0, padding='post', maxlen=25)

    # print(f"predict stuff: {model.predict(padded_sequence)}")


    return results, history


if __name__ == "__main__":
    data, labels = data_from_xml('md_full.xml')
    # print(f'{train_data[-1]}, {train_labels[-1]}')
    # test_data, test_labels = data_from_xml('test_full.xml')
    # print(f'{test_data[-1]}, {test_labels[-1]}')
    train_d, train_l, test_d, test_l, validation_d, validation_l = model_preprocessing(data, labels)
    result, history = create_model(train_d, train_l, test_d, test_l, validation_d, validation_l)
    print(f"The result is {result}")

    plot_loss(history)
    plot_accuracy(history)

    # with open('Testpage/Test/text_tokenizer.json', 'w') as f:
    #    f.write(json_string)

    # new_tokenizer = keras.preprocessing.text.tokenizer_from_json(json_string2)
