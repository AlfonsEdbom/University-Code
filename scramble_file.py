import random
# import nltk
from nltk.tokenize import sent_tokenize

"""
Scrambles a "inputfile" and saves it in "outputfile".
Outputfile contains 1 sentence per row w/o '.'

"""


def scramble(inputfile, outputfile="MyFileScrambeled.txt"):
    scrambled_list = []
    my_string = ""

    with open(inputfile, 'r') as fin:  # reads a file and creates string
        line_list = fin.readlines()
        for line in line_list:
            if line == "\n":  # handles newline rows
                continue
            else:
                formated_line = line.replace("\n", " ")
                my_string += formated_line

    tokens = sent_tokenize(my_string)  # create list containing each sentence

    for sentence in tokens:  # go through all sentences and scramble
        sentence_list = sentence[:-1].split(' ', )  # -1 to remove '.'
        sentence_list[0].lower()
        random.shuffle(sentence_list)
        sentence_string = ' '.join(sentence_list).strip().capitalize()
        scrambled_list.append(sentence_string)

    with open(outputfile, 'w') as fout:
        for line in scrambled_list:
            fout.write(line + '\n')


if __name__ == '__main__':
    scramble("text.txt", "scrambled_text.txt")
