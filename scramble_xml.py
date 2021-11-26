import random
from nltk.tokenize import sent_tokenize
from xml.dom import minidom

"""
Scrambles all sentences with a certain tag in inputfile and adds them with another tag at the end of inputfile".

"""


def scramble(inputfile, tag='sensical'):
    pass


def get_data(inputfile, tag="utterance"):
    """Gets all data with a tag in inputfile and returns each line to a list"""

    sentence_list = []
    dom = minidom.parse(inputfile)

    for qtag in dom.getElementsByTagName(tag):
        if qtag.getAttribute("sensical") == "true":
            my_string = qtag.getAttribute('text')
            sentence_list.append(my_string)

    return sentence_list


def scramble_sentences(sentence_list):
    scrambled_list = []
    for sentence in sentence_list:
        if sentence[-1] == '.': #TODO: Add how to keep, for example Mr. Biden as 1 word
            my_list = sentence[:-1].split(' ')
        else:
            my_list = sentence.split(' ')
        my_list[0] = my_list[0].lower()
        random.shuffle(my_list)
        my_list[0] = my_list[0].capitalize()
        sentence_string = ' '.join(my_list)
        scrambled_list.append(sentence_string)

    return scrambled_list

def scrambled_to_xml():
    pass #TODO: ADD this and look into maybe using ElementTree instead

def rest(inputfile, outputfile):
    scrambled_list = []



    with open(outputfile, 'w') as fout:
        for line in scrambled_list:
            fout.write(line + '\n')


if __name__ == '__main__':
    my_list = get_data("train_old.xml", "utterance")
    print(my_list)
    my_scrambled_list = scramble_sentences(my_list)
    print(my_scrambled_list)
