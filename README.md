# NLUClassifier
##The project

We have used tensorflow2 and Keras to create a machine learning model, and we have trained it on the NLTK Brown corpus. 
The purpose of the model is to somewhat accurately determine if a sentence is gibberish or if it actually makes sense.
We also created a simple website using Django, which allows you to enter a sentence to see if it is sensical or not.
##How to use

###Installation

Install the packages in the requirements.txt file using pip or any other preferred way.
###Data preprocessing

Under the "data" folder in the "Learning" repository we have different data sets for training and the main file to generate these.
* brown_full.xml
* empty.xml
* moby_dick_full.xml
* web_full.xml
* xml_processing.py

Xml files ending with _full is the complete corpus with sensical and non-sensical sentences.
Empty.xml is used in xml_processing.py to generate new datasets. 
Xml_processing.py is the main file used to download corpora form NLTK, store them as xml files that can be used to train the machine learning model.

###Training the model
Under the "Learning" repository we have:
* plots.py
* RNN_model.py
* xml_data.py

Plots.py and xml_data.py are files containing functions used to extract data from xml files and to plot
the loss and accuracy during the training process. RNN_model.py is the file containing our recurrent neural network model, it also
contains data preprocessing such as shuffling the data and dividing it into datasets used for training, validation and testing.
This is the file you run in order to train the model.



