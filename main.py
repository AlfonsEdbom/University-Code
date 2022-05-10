"""
Input: Genome sequence of a virus
"""

import json
import logging

from Fasta_DNA import Fasta_DNA
from Trie import Trie
from Filters import Filters
from Filter_Primers import Filter_Primers

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

    P2_genome = Fasta_DNA(config["files"]["P2"])

    primer_length = config["settings"]["length"]
    GC_min = config["settings"]["GC_min"]
    GC_max = config["settings"]["GC_max"]
    T_min = config["settings"]["T_min"]
    T_max = config["settings"]["T_max"]


    filter = Filter_Primers(P2_genome, Filters())

    filter.filter_GC_content(primer_length, GC_min, GC_max)
    t = filter.apply_filters(primer_length, T_min, T_max)


    test = t.query("")
    for i in test:
        logger.info(f"{i[0]}, {i[1]}")
    print(len(test))

    """
    for i in range(len(P2_f) - primer_length-1):
        primer = P2_f[i: i + primer_length]
        if not ("-" in primer):
            if GC_clamp(primer):
                if annealing_temp(primer, 55, 65):
                    t.insert(primer)
    for i in range(len(P2_rev) - primer_length-1):
        primer = P2_rev[i: i + primer_length]
        if not ("-" in primer):
            if GC_clamp(primer):
                if annealing_temp(primer, 55, 65):
                    t.insert(primer)
    """



if __name__ == '__main__':
    main()
