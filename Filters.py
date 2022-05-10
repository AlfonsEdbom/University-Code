import re


def calc_anneal_temp(sequence: str) -> float:
    anneal_temp = 0

    for base in sequence:
        if base in ["A", "T"]:
            anneal_temp += 2
        elif base in ["C", "G"]:  # Needs to be elif, since other char are gaps
            anneal_temp += 4

    return anneal_temp


class Filters:

    def annealing_temp(self, sequence: str, min_T: float, max_T: float):
        """Only keep primers /w appropriate Anneal_temp """
        seq_temp = calc_anneal_temp(sequence)

        if min_T < seq_temp < max_T:
            return sequence
        else:
            return False

    def remove_GCC(self, sequence, min_GC: float, max_GC: float) -> str:
        """Calculates the GC content of the input string"""
        num_G = sequence.count("G")
        num_C = sequence.count("C")
        num_A = sequence.count("A")
        num_T = sequence.count("G")

        num_GC = num_G + num_C
        num_AT = num_A + num_T

        GCC = num_GC / (num_GC + num_AT)

        if not (min_GC < GCC < max_GC):
            sequence = re.sub("[A-Z]", "-", sequence)

        return sequence

    def GC_clamp(self, sequence):
        """Removes primers that do not have a GC clamp"""
        end = sequence[-2:]

        if end in ["A", "T"]:
            return False
        else:
            return sequence

    def GC_end(self):
        """Only keep primers /w appropriate GC content in the end"""
        # 3 out 5 last are GC
