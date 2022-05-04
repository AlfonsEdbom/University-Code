"""
Input: Genome sequence of a virus
"""

import json

from Fasta_DNA import Fasta_DNA

def main():
    with open("config.json", "r") as c:
        config = json.load(c)

    print(config)
    P2_genome = Fasta_DNA(config["files"]["P2"])


    print(P2_genome.get_forward_strand())



if __name__ == '__main__':
    main()
