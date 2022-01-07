import random
from Learning import xml_data as ET
import nltk


def book_to_xml(book, n, fname_in, fname_out, offset=0):
    """
    Takes a book/text from an nltk predefined corpus and outputs sentences into a xml file
    No error handling for inappropriate indexing!
    :param fname_in: xml file to be parsed and added to
    :param book: nltk object , see nltk api reference for info
    :param n: number of sentences from the start to be gathered
    :param offset: how many sentences to skip in the document
    :param fname_out: name of the output file
    :return: xml file containing n sentences with start at offset
    """

    book_sentences = nltk.text.Text(book)

    xml_tree = ET.parse(fname_in)
    root = xml_tree.getroot()
    for i in book_sentences[offset: offset + n]:
        ET.SubElement(root, 'utterance', text=' '.join(i), sensical='true')

    ET.indent(xml_tree)
    xml_tree.write(fname_out, encoding='UTF-8', xml_declaration=True)


def get_data(inputfile, conditional_phrase='sensical', attribute='text'):
    """
    Gets the sensical sentences from a xml file, scrambles them and adds them to a list

    :param inputfile: The xml file to be read
    :param conditional_phrase: The attribute to be checked if true or false
    :param attribute: The attribute to be added to the output list
    :return: A list containing all sensical sentences in the input xml file.
    """

    tree = ET.parse(inputfile)
    root = tree.getroot()

    sentence_list = [child.get(attribute) for child in root if child.get(conditional_phrase) == 'true']

    return sentence_list


def scramble_sentences(sentence_list):
    """
    Scrambles all the sentences in the input list and returns them in a new list

    :param sentence_list: A list containing sensical sentences to be scrambled
    :return: A list containing the scrambled sentences
    """
    scrambled_list = []
    for sentence in sentence_list:
        if sentence[-1] == '.':
            word_list = sentence[:-1].split(' ')
        else:
            word_list = sentence.split(' ')

        word_list[0] = word_list[0].lower()
        random.shuffle(word_list)
        word_list[0] = word_list[0].capitalize()
        sentence_string = ' '.join(word_list)
        scrambled_list.append(sentence_string)

    return scrambled_list


def scrambled_to_xml(scrambled_list, fname_in, fname_out):
    """
    Adds a list of scrambled sentences into a existing xml file and outputs a new xml file
    :param scrambled_list: A list containing scrambled sentences
    :param fname_in: Name of the xml file the sentences will be added to
    :param fname_out: Name of the output xml file
    :return: A xml file containing both sensical and non-sensical sentences
    """
    xml_tree = ET.parse(fname_in)
    root = xml_tree.getroot()

    for sentence in scrambled_list:
        ET.SubElement(root, 'utterance', text=sentence, sensical='false')

    ET.indent(xml_tree)
    xml_tree.write(fname_out, encoding='UTF-8', xml_declaration=True)


if __name__ == '__main__':
    corpus = nltk.corpus.gutenberg.sents('melville-moby_dick.txt')
    corpus_len = len(corpus)
    corpus_half = corpus_len // 2

    # Train data of book[0:half]
    book_to_xml(book=corpus, n=corpus_len, offset=0,
                fname_in='empty.xml', fname_out='md.xml')
    book_list = get_data('md.xml')
    scrambled_list = scramble_sentences(book_list)
    scrambled_to_xml(scrambled_list, fname_in='md.xml',
                     fname_out='md_full.xml')

    # Test data of book[half: end]
    # book_to_xml(book=corpus, n=corpus_half, offset=corpus_half,
    #          fname_in='test.xml', fname_out='test_sensical.xml')
    # test_sensical_list = get_data('test_sensical.xml')
    # scrambled_test_list = scramble_sentences(test_sensical_list)
    # scrambled_to_xml(scrambled_test_list, fname_in='test_sensical.xml',
    #                 fname_out='test_full.xml')
