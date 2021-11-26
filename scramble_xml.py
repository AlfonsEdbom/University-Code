import random
from nltk.tokenize import sent_tokenize
from xml.dom import minidom
import xml.etree.ElementTree as ET

"""
Scrambles all sentences with a certain tag in inputfile and adds them with another tag at the end of another xml file".

"""


def scramble(inputfile, tag='sensical'):
    pass


def get_data(inputfile, conditional_phrase='sensical', attribute='text'):
    sentence_list = []
    tree = ET.parse(inputfile)
    root = tree.getroot()

    for child in root:
        if child.get(conditional_phrase) == 'true':
            sentence_list.append(child.get(attribute))
    return sentence_list


def scramble_sentences(sentence_list):
    scrambled_list = []
    for sentence in sentence_list:
        if sentence[-1] == '.':  # TODO: Add how to keep, for example Mr. Biden as 1 word, use nltk.tokenize.word mby
            my_list = sentence[:-1].split(' ')
        else:
            my_list = sentence.split(' ')
        my_list[0] = my_list[0].lower()
        random.shuffle(my_list)
        my_list[0] = my_list[0].capitalize()
        sentence_string = ' '.join(my_list)
        scrambled_list.append(sentence_string)

    return scrambled_list




def scrambled_to_xml(scrambled_list):
    # TODO: ADD this and look into maybe using ElementTree instead
    print(scrambled_list)
    tree = ET.parse('train_old.xml')
    root = tree.getroot()

    for sentence in scrambled_list:
        ET.SubElement(root, 'newutterance', text=sentence, sensical='false')

    tree.write('train_tested.xml', encoding='UTF-8', xml_declaration=True)
    #test = minidom.parse("train_tested.xml") #TODO: Might need use minidom to make nice doc again
    #test.toprettyxml())


def rest(inputfile, outputfile):
    scrambled_list = []

    with open(outputfile, 'w') as fout:
        for line in scrambled_list:
            fout.write(line + '\n')


def test_func():
    myTree = ET.parse('train_old.xml')
    myRoot = myTree.getroot()

    for child in myRoot:
        mystring = child.get('text')


def get_data_minidom(inputfile, tag="utterance"):
    """Gets all data with a tag in inputfile and returns each line to a list"""

    sentence_list = []
    dom = minidom.parse(inputfile)

    for qtag in dom.getElementsByTagName(tag):
        if qtag.getAttribute("sensical") == "true":
            my_string = qtag.getAttribute('text')
            sentence_list.append(my_string)

    return sentence_list


if __name__ == '__main__':
    my_list = get_data("train_old.xml")
    # print(my_list)
    my_scrambled_list = scramble_sentences(my_list)
    # print(my_scrambled_list)
    scrambled_to_xml(my_scrambled_list)
