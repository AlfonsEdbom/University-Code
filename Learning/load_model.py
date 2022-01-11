import tensorflow as tf

model = tf.keras.models.load_model('NLU_RNN_model/')

print('Done loading model')

testsent = ["This is a test sentence to see if the model can predict this"]

print(f"This is a test prediction: {model.predict(testsent)}")

