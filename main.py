import nltk
from xml.dom import minidom
import xml.etree.ElementTree as ET
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np




def keras_preprocessing():
    dom = minidom.parse("train_tested.xml")  # open .xml file

    sentence_list = [i.getAttribute('text') for i
                     in dom.getElementsByTagName("utterance")]  # only take text for vectorization

    max_features = 10000  # maximum vocab size
    max_sent_len = len(max(sentence_list, key=len).split())  # gets the length of longest sentence
    train_text = tf.constant(sentence_list)  # converts list to tensor containing text

    text_vectorizer = layers.TextVectorization(max_tokens=max_features,
                                               standardize="lower_and_strip_punctuation",
                                               output_mode="int",
                                               output_sequence_length=max_sent_len)  # create layer that does (str ->int)
    text_vectorizer.adapt(train_text)  # vectorize train_text

    # print(f"vocabulary used now: {text_vectorizer.get_vocabulary()}")

    # Create train_dataset
    dom2 = minidom.parse('train_tested.xml')
    train_list = [i.getAttribute('text') for i in dom2.getElementsByTagName('utterance')]
    train_sense = [1 if i.getAttribute('sensical') == 'true' else 0 for i in dom2.getElementsByTagName('utterance')]
    train_dataset = tf.data.Dataset.from_tensor_slices((train_list, train_sense))
    train_dataset = train_dataset.shuffle(len(train_dataset))

    # Create test_dataset
    dom3 = minidom.parse('test.xml')
    test_list = [i.getAttribute('text') for i in dom3.getElementsByTagName('utterance')]
    test_sense = [1 if i.getAttribute('sensical') == 'true' else 0 for i in dom3.getElementsByTagName('utterance')]
    test_cutoff = len(test_list) // 2
    test_dataset = tf.data.Dataset.from_tensor_slices(
        (test_list[:test_cutoff], test_sense[:test_cutoff]))  # TODO Shuffle these somehow
    validation_dataset = tf.data.Dataset.from_tensor_slices((test_list[test_cutoff:], test_sense[test_cutoff:]))

    # Create model
    embedding_dim = 16
    model = tf.keras.Sequential()
    model.add(layers.Embedding(max_features, embedding_dim))
    model.add(layers.GlobalAveragePooling1D())
    model.add(layers.Dense(1))

    model.summary()

    model.compile(loss='binary_crossentropy',
                  optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  metrics=['accuracy'])

    epochs = 10
    history = model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=epochs)

    """
    inputs = keras.Input(shape=(None, ), dtype="int64") #what inputs the model will accept

    #WTF is this?!?!?
    x = layers.Embedding(input_dim=text_vectorizer.vocabulary_size(),
                         output_dim=16)(inputs) #turns indexes into dense vector of
    x = layers.GRU(8)(x)
    outputs = layers.Dense(1)(x)

    #WTF is this?!?!? ends

    model = keras.Model(inputs, outputs)

    dom2 = minidom.parse('train_tested.xml')
    train_list = [i.getAttribute('text') for i
                  in dom2.getElementsByTagName('utterance')]

    train_sense = [1 if i.getAttribute('sensical') == 'true' else 0
                   for i in dom2.getElementsByTagName('utterance')]

    train_dataset = tf.data.Dataset.from_tensor_slices((train_list, train_sense))

    train_dataset = train_dataset.batch(2).map(lambda x, y: (text_vectorizer(x), y))
    print(''\nTraining model...')
    model.compile(optimizer='rmsprop", loss="mse')
    model.fit(train_dataset)
    #model = tf.keras.models.Sequential()
    #model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
    #model.add(text_vectorizer)


    #print(f"Encoded text:\n {text_vectorizer(['give me the cities in blahblah']).numpy()}")
    """


def file_to_dict(filename):
    """
    Creates dictionaries to transform words into integers and then back again
    File should be a .xml file created with scramble_file/xml.py
    """
    dom = minidom.parse(filename)
    text_list = []
    sense_list = []

    # get all sentences from file
    for qtag in dom.getElementsByTagName("utterance"):
        my_text = qtag.getAttribute('text').lower().strip()
        if my_text[-1] == '.':  # remove '.' if present at end of sentence
            my_text = my_text[: -1]
        my_text_words = my_text.split(' ')  # splits sentence into words
        my_sense = qtag.getAttribute('sensical')  # gets if sensical is true or false

        text_list.append(my_text_words)  # adds all words to a list
        sense_list.append(my_sense)  # adds all sensical to a list

    # makes text_list into a list of just words instead of list of lists
    word_list = []
    for sentence_list in text_list:
        for word in sentence_list:
            word_list.append(word)

    # makes dict containing each word and how many times occured, then sorts in descending order
    word_dict = dict([(i, word_list.count(i)) for i in set(word_list)])
    words_sorted_tuples = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)

    # transforms the tuples back into dict
    sorted_word_dict = {}
    for k, v in words_sorted_tuples:
        sorted_word_dict[k] = v

    word_index = {}
    for count, k in enumerate(sorted_word_dict):
        word_index[k] = count

    word_index = {k: (v + 4) for k, v in word_index.items()}
    word_index['<PAD>'] = 0
    word_index['<START>'] = 1
    word_index['<UNK>'] = 2
    word_index['<UNUSED>'] = 3

    reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
    return word_index, reverse_word_index


def file_to_list(word_index, reverse_word_index, filename):
    """
    Gets train_data/labels and test_data/labels
    """

    dom_train = minidom.parse(filename)
    dom_test = minidom.parse("test.xml")

    sentence_list = []  # contanins all words translated into integers
    sense_list = []  # contains all senses translated into 1 for 'true' and 0 for 'false'
    for qtag in dom_train.getElementsByTagName("utterance"):
        my_string = qtag.getAttribute('text')
        word_list = my_string.split(' ')
        word_list.insert(0, '<START>')
        for count, word in enumerate(word_list):
            if word not in word_index.keys():
                word_list[count] = word_index["<UNK>"]
            else:
                word_list[count] = word_index[word]

        sentence_list.append(word_list)

        my_sense = qtag.getAttribute('sensical')
        if my_sense == 'true':
            my_sense = 1
        if my_sense == 'false':
            my_sense = 0
        sense_list.append(my_sense)
    # print(len(sentence_list))
    # print(len(sense_list))
    return sentence_list, sense_list


def make_model(train_data, train_labels, test_data, test_labels):
    # print(len(train_data[0]), len(train_data[10]))
    np.asarray(train_labels)
    test_data = np.array(test_data)
    test_labels = np.array(test_labels)

    indices = np.arange(test_data.shape[0])
    np.random.shuffle(indices)
    test_data = test_data[indices]
    test_labels = test_labels[indices]

    train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                            value=word_index['<PAD>'],
                                                            padding='post',
                                                            maxlen=20)
    test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                           value=word_index['<PAD>'],
                                                           padding='post',
                                                           maxlen=20)

    print(len(test_data))
    print(len(test_labels))
    vocab_size = 1000

    model = keras.Sequential()
    model.add(keras.layers.Embedding(vocab_size, 16))  # every word get vectorized in 16 dimensions
    model.add(keras.layers.GlobalAveragePooling1D())  # flattens 16D vector to 1D vector
    model.add(keras.layers.Dense(16, activation=tf.nn.relu))  # 16 nodes for 16 dimensions, first NN layer
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))  # 1 node layer, gives us a value between 0 and 1

    model.summary()

    # optimizer and loss function
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    x_val = train_data[:100]
    partial_x_train = train_data[100:]

    y_val = train_labels[:100]
    partial_y_train = train_labels[100:]

    np.asarray(x_val)
    np.asarray(partial_y_train)
    y_val = np.array(y_val)
    partial_y_train = np.array(partial_y_train)

    # print(len(x_val))
    # print(len(partial_x_train))
    # print(len(y_val))
    # print(len(partial_y_train))

    history = model.fit(partial_x_train,
                        partial_y_train,
                        epochs=40,
                        batch_size=512,
                        validation_data=(x_val, y_val),
                        verbose=1)
    print(len(test_data))
    print(len(test_labels))
    results = model.evaluate(test_data, test_labels)
    print(f'Results: {results}')



if __name__ == "__main__":
    word_index, reverse_word_index = file_to_dict("train_tested.xml")
    # print(word_index)
    # keras_preprocessing()
    #x_d, x_l = file_to_list(word_index, reverse_word_index, "train_tested.xml")
    #y_d, y_l = file_to_list(word_index, reverse_word_index, "test.xml")
    #make_model(x_d, x_l, y_d, y_l)
