import numpy as np
import tensorflow as tf
from tensorflow import keras
import os

from plots import plot_loss, plot_accuracy
from xml_data import get_data


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
    train_cutoff = int(len(data) * 0.75)  # how much
    test_cutoff = int(len(data) * 1)

    train_data = np.asarray(shuffled_data[0: train_cutoff])  # from 0 to train_cutoff
    train_labels = np.asarray(shuffled_labels[0: train_cutoff])

    test_data = np.asarray(shuffled_data[train_cutoff: test_cutoff])  # from train_cutoff to test_cutoff
    test_labels = np.asarray(shuffled_labels[train_cutoff: test_cutoff])

    validation_data = np.asarray(shuffled_data[train_cutoff: -1])  # from test_cutoff to end
    validation_labels = np.asarray(shuffled_labels[train_cutoff: -1])

    # create word to int dict and reverse
    VOCAB_SIZE = 1000
    encoder = tf.keras.layers.TextVectorization(max_tokens=VOCAB_SIZE)
    encoder.adapt(train_data)
    vocab = np.array(encoder.get_vocabulary())
    vocab[:20]

    return train_data, train_labels, test_data, test_labels, validation_data, validation_labels, encoder


def create_RNN_model(train_data, train_labels, test_data, test_labels, validation_data, validation_labels, encoder):
    model = tf.keras.Sequential([
        encoder,
        tf.keras.layers.Embedding(
            input_dim=len(encoder.get_vocabulary()),
            output_dim=64,
            mask_zero=True),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1)])

    model.summary()

    # compile model
    model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  optimizer=tf.keras.optimizers.Adam(1e-4),
                  metrics=['accuracy'])

    # Fit the model

    history = model.fit(train_data,
                        train_labels,
                        epochs=10,
                        batch_size=64,
                        validation_data=(validation_data, validation_labels),
                        verbose=1)

    results = model.evaluate(test_data, test_labels)

    #model.save('NLU_RNN_model/') #needed to export model

    return results, history


if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    data_file = 'web_full.xml'
    data_path = os.path.join(data_dir, data_file)

    data, labels = get_data(data_path)
    train_d, train_l, test_d, test_l, validation_d, validation_l, encoder = model_preprocessing(data, labels)
    result, history = create_RNN_model(train_d, train_l, test_d, test_l, validation_d, validation_l, encoder)
    print(f"The result is {result}")

    plot_loss(history)
    plot_accuracy(history)

    # with open('Testpage/Test/text_tokenizer.json', 'w') as f:
    #    f.write(json_string)
