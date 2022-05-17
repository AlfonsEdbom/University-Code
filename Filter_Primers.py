from Filters import Filters
from Fasta_DNA import Fasta_DNA

from Trie import Trie


class Filter_Primers:
    """
    Class with methods for removing primers that are determined to
    not be a candidate PCR-primer
    """

    def __init__(self, genome: Fasta_DNA):
        self.forward = genome.get_forward_strand()  # forward strand of DNA
        self.reverse = genome.get_reverse_strand()  # reverse strand of DNA
        self.filters = Filters()  # Filter object, with contains the logics for the filters
        self.forward_primers = []  # List of primers deemed to candidate forward PCR-primers
        self.reverse_primers = []  # List of primers deemed to be candidate reverse PCR-primers

    def filter_GC_content(self, primer_length: int, GC_min: float, GC_max: float) -> None:
        """
        Replaces regions of the DNA with too high/low GC-content  with a '-'
        These regions will not be considered by the other functions
        """
        # Create windows of size primer length for GC_content analysis
        forward_list = [self.forward[i:i + primer_length]
                        for i in range(0, len(self.forward), primer_length)]
        reverse_list = [self.reverse[i:i + primer_length]
                        for i in range(0, len(self.reverse), primer_length)]

        # Replaces bases with '-' if outside min and max
        for i, primer in enumerate(forward_list):
            primer = self.filters.remove_GCC(primer, GC_min, GC_max)
            forward_list[i] = primer

        for i, primer in enumerate(reverse_list):
            primer = self.filters.remove_GCC(primer, GC_min, GC_max)
            reverse_list[i] = primer

        # Rewrites the DNA-string with the GC-regions removed
        self.forward = "".join(forward_list)
        self.reverse = "".join(reverse_list)

    def apply_filters(self, primer_length: int, min_T: float, max_T: float):
        """
        Applies the filters found in Filters.py to all primers found in the genome
        Saves them in the list of candidate PCR-primers
        """

        for i in range(len(self.forward) - primer_length + 1):
            primer = self.forward[i:i + primer_length]
            if not ("-" in primer):
                if self.filters.GC_clamp(primer):
                    if self.filters.annealing_temp(primer, min_T, max_T):
                        tmplist = [primer, (i, i + primer_length)]
                        self.forward_primers.append(tmplist)

        for i in range(len(self.reverse) - primer_length + 1):
            primer = self.reverse[i:i + primer_length]
            if not ("-" in primer):
                if self.filters.GC_clamp(primer):
                    if self.filters.annealing_temp(primer, min_T, max_T):
                        tmplist = [primer, (-i, -(i + primer_length))]
                        self.reverse_primers.append(tmplist)

    def remove_similar(self, trie: Trie, max_mismatches: int):
        """
        Removes primers from self.candidate_primers that have too binding temp.

        """

        tmp_forward = []
        for primer in self.forward_primers:
            sequence = primer[0]
            similar_list = trie.search_hamming_dist(sequence, max_mismatches)
            if not similar_list:
                tmp_forward.append(primer)

        tmp_reverse = []
        for primer in self.reverse_primers:
            sequence = primer[0]
            similar_list = trie.search_hamming_dist(sequence, max_mismatches)
            if not similar_list:
                tmp_reverse.append(primer)

        self.forward_primers = tmp_forward
        self.reverse_primers = tmp_reverse

    def get_primer_pairs(self, primer_length):
        #for p, i in zip(self.candidate_primers, self.candidate_primers_index):
         #   print(p)
          #  print(i)
        pass