import re


def is_complimentary(base1: str, base2: str) -> tuple[bool, int]:
    """
    Returns True if base1 and base2 are complimentary to each other
    and the annealing temperature gain from the match
    """
    if base1 == "A" and base2 == "T":
        return True, 2
    elif base1 == "T" and base2 == "A":
        return True, 2
    elif base1 == "G" and base2 == "C":
        return True, 4
    elif base1 == "C" and base2 == "G":
        return True, 4
    else:
        return False, 0


def calc_anneal_temp(sequence: str) -> int:
    """
    Calculates the annealing temperature for a sequence
    A, T = +2
    G, C = +4
    Returns the annealing temperature for the sequence
    """
    anneal_temp = 0

    for base in sequence:
        if base in ["A", "T"]:
            anneal_temp += 2
        elif base in ["C", "G"]:
            anneal_temp += 4

    return anneal_temp


class Filters:

    def remove_GCC(self, sequence, min_GC: int, max_GC: int) -> str:
        """
        Replaces the sequence with '-' if too high or low GC content in the primer
        min_GC and max_GC should be ints in percentages
        Returns either the sequence or a string with '-'
        """
        num_G = sequence.count("G")
        num_C = sequence.count("C")
        num_A = sequence.count("A")
        num_T = sequence.count("T")

        num_GC = num_G + num_C
        num_AT = num_A + num_T

        GCC = num_GC / (num_GC + num_AT)

        if not (min_GC / 100) < GCC < (max_GC / 100):
            sequence = re.sub("[A-Z]", "-", sequence)

        return sequence

    def annealing_temp(self, sequence: str, min_T: int, max_T: int) -> bool:
        """
        Returns False if sequence annealing temp. is not within min_T and max_T
        Otherwise True is returned
        """
        seq_temp = calc_anneal_temp(sequence)

        if min_T < seq_temp < max_T:
            return True
        else:
            return False

    def GC_clamp(self, sequence: str) -> bool:
        """
        Returns False if the sequence does not have a G or C in the last 2 positions
        Otherwise True is returned
        """
        end1 = sequence[-1]
        end2 = sequence[-2]

        if end1 in ["A", "T"] or end2 in ["A", "T"]:
            return False
        else:
            return True

    def GC_end(self, sequence: str, end_num: int = 5, max_GC: int = 3) -> bool:
        """
        Returns False if more than 3 of the 5 last positions is a G or C
        Otherwise True is returned
        """
        # 3 out 5 last are GC
        end = sequence[-end_num:]

        num_G = end.count("G")
        num_C = end.count("C")

        num_GC = num_G + num_C

        if num_GC > max_GC:
            return False
        else:
            return True

    def self_dimerisation(self, sequence: str, max_temp: int = 10) -> bool:
        """
        Returns False if the sequence can dimerize with itself
        Otherwise True is returned
        """

        reverse = sequence[::-1]  # Create copy of sequence to test dimerize
        for i in range(len(sequence)):  # start at beginning of sequence
            temperature = 0  # Reset the temperature each loop in the original strand
            for j in range(len(reverse)):  # go through every position of second sequence on first
                match, cost = is_complimentary(sequence[i], reverse[j])  # check if first and second match
                if match:  # if they match
                    # temporary index variables
                    tmp_i = i
                    tmp_j = j

                    temperature += cost  # increase temp depending on which bases match
                    while match:  # Go forward on each strand to check if continue matching
                        if tmp_i == len(sequence) - 1 or tmp_j == len(
                                reverse) - 1:  # break if the end of a sequnece is reached
                            break
                        tmp_i += 1
                        tmp_j += 1
                        match, cost = is_complimentary(sequence[tmp_i], reverse[tmp_j])  # check if they match
                        if match:  # increase temperature if they match
                            temperature += cost
                        else:  # if they dont match, reset temperature and exit while loop
                            temperature = 0

                        if temperature > max_temp:  # If bind above max_temp, it can self-dimerize
                            return False  # Dont use this primer
                else:  # if dont match, reset the temperature and go to next in second loop
                    temperature = 0
        return True  # returns if entire sequence goes through without getting over max_temp

    def inter_dimerisation(self, sequence1: str, sequence2: str, max_temp: int = 10):
        reverse_second = sequence2[::-1]  # Create copy of sequence to test dimerize
        for i in range(len(sequence1)):  # start at beginning of sequence
            temperature = 0  # Reset the temperature each loop in the original strand
            for j in range(len(sequence2)):  # go through every position of second sequence on first
                match, cost = is_complimentary(sequence1[i], sequence2[j])  # check if first and second match
                if match:  # if they match
                    # temporary index variables
                    tmp_i = i
                    tmp_j = j

                    temperature += cost  # increase temp depending on which bases match
                    while match:  # Go forward on each strand to check if continue matching
                        if tmp_i == len(sequence1) - 1 or tmp_j == len(
                                sequence2) - 1:  # break if the end of a sequnece is reached
                            break
                        tmp_i += 1
                        tmp_j += 1
                        match, cost = is_complimentary(sequence1[tmp_i], sequence2[tmp_j])  # check if they match
                        if match:  # increase temperature if they match
                            temperature += cost
                        else:  # if they dont match, reset temperature and exit while loop
                            temperature = 0

                        if temperature > max_temp:  # If bind above max_temp, it can self-dimerize
                            return False  # Dont use this primer
                else:  # if dont match, reset the temperature and go to next in second loop
                    temperature = 0
        return True  # returns if entire sequence goes through without getting over ma
