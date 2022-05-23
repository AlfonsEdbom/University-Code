"""
Input: Genome sequence of a virus
"""

import time
from datetime import timedelta

import json
import logging

from Fasta_DNA import Fasta_DNA
from Candidate_Primers import Candidate_Primers


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

def write_pp_to_file(file_name: str, primer_pairs) -> None:
    with open(file_name, "w") as of:
        of.write("Primer pairs: Forward primer, Reverse primer, Contig length \n")
        for primer_pair in primer_pairs:
            of.write(f"{primer_pair[0].sequence}, {primer_pair[1].sequence}, "
                     f"{primer_pair[2]} ({primer_pair[0].start}-{primer_pair[0].start+primer_pair[2]})\n")


def main():
    start_time = time.monotonic()  # Start timer for program

    # Load config settings from config.json and initiate logger
    config = get_config("config.json")
    logger = get_logger("log.log")
    
    # Set settings from config file to variables
    primer_length = config["settings"]["length"]
    GC_min = config["settings"]["GC_min"]
    GC_max = config["settings"]["GC_max"]
    T_min = config["settings"]["T_min"]
    T_max = config["settings"]["T_max"]
    deltaT = config["settings"]["deltaT"]
    GC_window = config["settings"]["GC_window"]
    
    # Create DNA-object containing DNA in Fasta file
    genome_DNA = Fasta_DNA(config["files"]["SARS"])

    # Build a trie containing all primers of specific length (f and r)
    t = genome_DNA.build_primer_Trie(primer_length)
    logger.debug(f"The Trie contains {len(t.query(''))} primers!")
    logger.debug(f"Primer Trie built successfully: {timedelta(seconds=time.monotonic() - start_time)}")

    candidate_primers = Candidate_Primers(genome_DNA)  # initiate filter object

    candidate_primers.filter_GC_content(GC_window, GC_min, GC_max)  # remove windows with too high GC-content
    logger.debug(f"GC content filter has been applied! {timedelta(seconds=time.monotonic() - start_time)}")

    candidate_primers.apply_filters(primer_length, T_min, T_max)  # Apply the rest of the filteres
    logger.debug(f"The rest of the filters has been applied! {timedelta(seconds=time.monotonic() - start_time)}")
    print(len(candidate_primers.forward_primers))
    print(len(candidate_primers.reverse_primers))

    candidate_primers.remove_similar(t, deltaT)  # Remove primers with too low deltaT
    #print(len(candidate_primers.forward_primers))
    #print(len(candidate_primers.reverse_primers))
    logger.debug(f"deltaT filter has been applied! {timedelta(seconds=time.monotonic() - start_time)}")
    logger.debug(f"forward_strand: {candidate_primers.forward}")
    primer_pairs = candidate_primers.get_primer_pairs(300, 1500)
    primer_pairs = candidate_primers.filter_primer_pairs(primer_pairs, GC_min, GC_max)

    logger.debug(primer_pairs)
    logger.debug(len(primer_pairs))
    write_pp_to_file("output.txt", primer_pairs)
    print(f"The program took {timedelta(seconds=time.monotonic() - start_time)} to execute)")


if __name__ == '__main__':
    main()
