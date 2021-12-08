import tensorflow as tf
from tensorflow import keras
import numpy as np

print(tf.__version__)
'''
This model is taken from a tutorial made by the tensorflow team, i think we can use this very basic model as a 
foundation for our model. 
'''

# imdb dataset that comes with keras
imdb = keras.datasets.imdb
# assigning the data and labels to variables, num_words are the 10000 most popular words used
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

# printing out the second item in train_data and tran_labels
print(train_data[1], train_labels[1])
# printing out the length of the first and second item before padding/standardization
print('\n', len(train_data[0]), len(train_data[1]))

# The dict mapping words to integers
word_index = imdb.get_word_index()

# The first indices are reserved for padding, start, unknown and unused
word_index = {k: (v+3) for k, v in word_index.items()}
word_index['<PAD>'] = 0
word_index['<START>'] = 1
word_index['<UNK>'] = 2
word_index['<UNUSED>'] = 3

# swaps the words (keys) with their numbers (values)
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])


# prints out the decoded text, we can take the number representation and get the original text
def decode_review(text):
    return ' '.join([reverse_word_index.get(i, '?') for i in text])


# here we're adjusting the lengths of the items to a maximum of 256
# longer items get shortened and too short items gets padded with 0s at the end of the item
train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                        value=word_index['<PAD>'],
                                                        padding='post',
                                                        maxlen=256)
test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                       value=word_index['<PAD>'],
                                                       padding='post',
                                                       maxlen=256)

# prints out the length of the first and second item in train_data after padding/standardization
print(len(train_data[0]), len(train_data[1]))

# Building the model
vocab_size = 10000

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

# dividing data into training data and validation data, 10k/15k split for validation/training
x_val = train_data[:10000]
partial_x_train = train_data[10000:]

y_val = train_labels[:10000]
partial_y_train = train_labels[10000:]

# training the model, epochs = 40 -> 40 rounds of training, batch_size = 512 -> model takes 512 items at a time
history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=40,
                    batch_size=512,
                    validation_data=(x_val, y_val),
                    verbose=1)

results = model.evaluate(test_data, test_labels)
print('Results: ', results)
