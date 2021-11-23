import random
import nltk
from nltk.tokenize import sent_tokenize


def scramble(inputfile, outputfile="MyFileScrambeled.txt"):
    scrambled_list = []
    my_string = ""

    with open(inputfile, 'r') as fin:  # reads a file and creates string
        line_list = fin.readlines()
        for line in line_list:
            formated_line = line.replace("\n", " ")
            my_string += formated_line

    tokens = sent_tokenize(my_string)  # create list containing each sentence

    for sentence in tokens:  # go through all sentences and scramble
        sentence_list = sentence.split(' ')
        random.shuffle(sentence_list)
        [scrambled_list.append(word) for word in sentence_list]

    # Some very ugly formatting for it be readable.
    if scrambled_list[0].islower():
        scrambled_list[0] = scrambled_list[0].capitalize()
        print(scrambled_list[0])

    for i in range(1, len(scrambled_list)):
        if scrambled_list[i - 1][-1] == '.':
            scrambled_list[i] = scrambled_list[i].capitalize()

        if scrambled_list[i].isupper():
            if scrambled_list[i - 1][-1] != '.':
                scrambled_list[i] = scrambled_list[i][0].lower()

    with open(outputfile, 'w') as fout:
        for line in scrambled_list:
            fout.write(line + ' ')


if __name__ == '__main__':
    scramble("text.txt", "scrambled_text.txt")
