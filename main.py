"""
Input: Genome sequence of a virus
"""

import json
import logging

from Fasta_DNA import Fasta_DNA
from Trie import Trie
from Filters import Filters, remove_GCC


def get_config(config_file: str) -> dict:
    with open(config_file, "r") as c:
        config = json.load(c)

    return config


def get_logger(log_file: str):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")

    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def main():
    config = get_config("config.json")
    logger = get_logger("log.log")

    t = Trie()
    P2_genome = Fasta_DNA(config["files"]["P2"])

    P2_f = P2_genome.get_forward_strand()
    P2_rev = P2_genome.get_reverse_strand()

    PRIMER_LENGTH = config["settings"]["length"]
    GC_MAX = config["settings"]["GC_max"]
    GC_MIN = config["settings"]["GC_min"]

    P2_flist = [P2_f[i:i+PRIMER_LENGTH] for i in range(0, len(P2_f), PRIMER_LENGTH)]


    for i, primer in enumerate(P2_flist):
        primer = remove_GCC(primer, GC_MIN, GC_MAX)

        P2_flist[i] = primer

        #logger.info(primer)


    P2_f = "".join(P2_flist)

    for i in range(len(P2_f) - PRIMER_LENGTH-1):
        primer = P2_f[i: i + PRIMER_LENGTH]
        if not ("-" in primer):
            t.insert(primer)

    for i in range(len(P2_rev) - PRIMER_LENGTH-1):
        primer = P2_rev[i:i + PRIMER_LENGTH]
        if not("-" in primer):
            t.insert(primer)

    test = t.query("")
    for i in test:
        logger.info(f"{i[0]}, {i[1]}")
    print(len(test))

if __name__ == '__main__':
    main()
