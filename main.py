"""
Input: Genome sequence of a virus
"""

import json

from Fasta_DNA import Fasta_DNA

def main():
    with open("config.json", "r") as c:
        config = json.load(c)

    test = Fasta_DNA(config["filename"])
    test2 = Fasta_DNA(config["filename2"])

    print(test.get_forward_strand())
    print(test2.get_forward_strand())


if __name__ == '__main__':
    main()
