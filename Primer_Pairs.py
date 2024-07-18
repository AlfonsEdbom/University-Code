from Candidate_Primers import Primer
from Fasta_DNA import Fasta_DNA
from Filters import Filters

import re

restriction_enzymes = {"BAMHI":
                           {"site": "GGATCC", "cut": 1},
                       "EcoRI":
                           {"site": "GAATTC", "cut": 1},
                       "HINDIII":
                           {"site": "AAGCTT", "cut": 1},
                       "NotI":
                           {"site": "GCGGCCGC", "cut": 2},
                       "XbaI":
                           {"site": "TCTAGA", "cut": 1}
                       }


def restriction_cut(restriction_enzyme, sequence, length) -> list:
    restriction_list = []
    pattern = rf"({restriction_enzymes[restriction_enzyme]['site']})"
    matches = re.finditer(pattern, sequence)
    fragment_start = 0
    for match in matches:
        cut_pos = match.span()[0] + restriction_enzymes[restriction_enzyme]["cut"]

        restriction_list.append((fragment_start, cut_pos))
        fragment_start = cut_pos + 1

    restriction_list.append((fragment_start, length))

    return restriction_list


class Primer_Pairs:
    def __init__(self, DNA: Fasta_DNA, forward_primers: list[Primer], reverse_primers: list[Primer]) -> None:
        self.forward_primers = forward_primers
        self.reverse_primers = reverse_primers
        self.DNA = DNA

        self.filters = Filters()
        self.primer_pairs = []  #

    def find_primer_pairs(self, min_dist, max_dist, is_circular: bool = True):
        for forward_primer in self.forward_primers:
            for reverse_primer in self.reverse_primers:
                forward_pos = forward_primer.start
                reverse_pos = len(self.DNA.reverse_strand) + reverse_primer.start  # reformat to be in forward position

                distance = reverse_pos - forward_pos

                if min_dist < distance < max_dist:
                    self.primer_pairs.append([forward_primer, reverse_primer, distance])

                if is_circular:

                    overlapping_dist = len(self.DNA.forward_strand) + distance

                    if min_dist < overlapping_dist < max_dist:
                        self.primer_pairs.append([forward_primer, reverse_primer, overlapping_dist])

    def filter_primer_pairs(self, min_GC: int, max_GC: int):
        tmp_primers = []
        for primer_pair in self.primer_pairs:
            forward_primer = primer_pair[0]
            reverse_primer = primer_pair[1]
            distance = primer_pair[2]

            if self.filters.inter_dimerisation(forward_primer.sequence, reverse_primer.sequence):
                start_pos = forward_primer.start
                end_pos = forward_primer.start + distance

                contig = self.DNA.forward_strand[start_pos:end_pos]
                num_G = contig.count("G")
                num_C = contig.count("C")
                num_A = contig.count("A")
                num_T = contig.count("T")

                num_GC = num_G + num_C
                num_AT = num_A + num_T

                GCC = num_GC / (num_GC + num_AT)

                if (min_GC / 100) < GCC < (max_GC / 100):
                    tmp_primers.append(primer_pair)

        self.primer_pairs = tmp_primers

    def restriction_enzymes_cut(self, BAMHI=True, EcoRI=True, HINDIII=True, NotI=True, XbaI=True):

        for i, primer_pair in enumerate(self.primer_pairs):
            forward_primer = primer_pair[0]
            contig_length = primer_pair[2]

            contig_start = forward_primer.start
            contig_end = contig_start + contig_length
            contig_sequence = self.DNA.forward_strand[contig_start:contig_end]

            if BAMHI:
                BAMHI_list = restriction_cut("BAMHI", contig_sequence, contig_length)
                self.primer_pairs[i].append(BAMHI_list)

            if EcoRI:
                ECORI_list = restriction_cut("EcoRI", contig_sequence, contig_length)
                self.primer_pairs[i].append(ECORI_list)

            if HINDIII:
                HINDIII_list = restriction_cut("HINDIII", contig_sequence, contig_length)
                self.primer_pairs[i].append(HINDIII_list)

            if NotI:
                NotI_list = restriction_cut("NotI", contig_sequence, contig_length)
                self.primer_pairs[i].append(NotI_list)

            if XbaI:
                XbaI_list = restriction_cut("XbaI", contig_sequence, contig_length)
                self.primer_pairs[i].append(XbaI_list)

    def get_primer_pairs(self, sort_index = 2):
        if sort_index > 2:
            return sorted(self.primer_pairs, key=lambda x: len(x[sort_index]), reverse=True)
        else:
            return sorted(self.primer_pairs, key=lambda x: x[sort_index], reverse=True)