import nltk
from xml.dom import minidom
from collections import Counter


def weeble_wobble():
    dom = minidom.parse("train.xml")

    for qtag in dom.getElementsByTagName("utterance"):
        if qtag.getAttribute("sensical") == "true":
            print(f"{qtag.getAttribute('text')} makes sense")
        else:
            print(f"{qtag.getAttribute('text')} is weird")


def test():
    """
    Creates dictionaries to transform words into integers and then back again
    File should be a .xml file
    """
    dom = minidom.parse("train_tested.xml")  # TODO CHANGE FILENAME
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

def test2(word_index, reverse_word_index, filename):
    """
    Gets train_data/labels and test_data/labels
    """

    dom_train = minidom.parse(filename)
    dom_test = minidom.parse("test.xml")

    sentence_list = [] #contanins all words translated into integers
    sense_list = [] #contains all senses translated into 1 for 'true' and 0 for 'false'
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

    return sentence_list, sense_list



if __name__ == "__main__":
    word_index, reverse_word_index = test()
    train = test2(word_index, reverse_word_index, "train_tested.xml")
    test = test2(word_index, reverse_word_index, "test.xml")




