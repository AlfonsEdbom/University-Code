"""
Input: Genome sequence of a virus
"""

import json
import logging

import time
from datetime import timedelta

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
    start_time = time.monotonic()

    config = get_config("config.json")
    logger = get_logger("log.log")

    P2_genome = Fasta_DNA(config["files"]["test"])

    primer_length = config["settings"]["length"]
    GC_min = config["settings"]["GC_min"]
    GC_max = config["settings"]["GC_max"]
    T_min = config["settings"]["T_min"]
    T_max = config["settings"]["T_max"]
    deltaT = config["settings"]["deltaT"]

    t = P2_genome.build_primer_Trie(primer_length)
    logger.debug(f"Primer Trie built! {timedelta(seconds=time.monotonic() - start_time)}")

    remove_primers = Filter_Primers(P2_genome)

    remove_primers.filter_GC_content(primer_length, GC_min, GC_max)
    logger.debug(f"GC content filter has been applied! {timedelta(seconds=time.monotonic() - start_time)}")
    candidate_primers, candidate_indices = remove_primers.apply_filters(primer_length, T_min, T_max)
    logger.debug(f"The rest of the filters has been applied! {timedelta(seconds=time.monotonic() - start_time)}")
    similar_primers, similar_indices = remove_primers.remove_similar(t, deltaT)
    logger.debug(f"deltaT filter has been applied! {timedelta(seconds=time.monotonic() - start_time)}")

    remove_primers.get_primer_pairs(1)
    logger.debug(len(candidate_primers))
    logger.debug(len(similar_primers))


    print(f"The program took {timedelta(seconds=time.monotonic() - start_time)} to execute)")



if __name__ == '__main__':
    main()
