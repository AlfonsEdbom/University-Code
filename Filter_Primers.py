from Filters import Filters
from Fasta_DNA import Fasta_DNA
from Trie import Trie


class Filter_Primers:
    def __init__(self, genome: Fasta_DNA):
        self.forward = genome.get_forward_strand()
        self.reverse = genome.get_reverse_strand()
        self.filters = Filters()
        self.primer_trie = Trie()

    def filter_GC_content(self, primer_length: int, GC_min: float, GC_max: float) -> None:
        forward_list = [self.forward[i:i + primer_length]
                        for i in range(0, len(self.forward), primer_length)]
        reverse_list = [self.reverse[i:i + primer_length]
                        for i in range(0, len(self.reverse), primer_length)]

        for i, primer in enumerate(forward_list):
            primer = self.filters.remove_GCC(primer, GC_min, GC_max)
            forward_list[i] = primer

        for i, primer in enumerate(reverse_list):
            primer = self.filters.remove_GCC(primer, GC_min, GC_max)
            reverse_list[i] = primer

        self.forward = "".join(forward_list)
        self.reverse = "".join(reverse_list)

    def apply_filters(self, primer_length: int, min_T, max_T):
        for i in range(len(self.forward) - primer_length - 1):
            primer = self.forward[i:i + primer_length]
            if not ("-" in primer):
                if self.filters.GC_clamp(primer):
                    if self.filters.annealing_temp(primer, min_T, max_T):
                        self.primer_trie.insert(primer)

        for i in range(len(self.reverse) - primer_length - 1):
            primer = self.reverse[i:i + primer_length]
            if not ("-" in primer):
                if self.filters.GC_clamp(primer):
                    if self.filters.annealing_temp(primer, min_T, max_T):
                        self.primer_trie.insert(primer)

        return self.primer_trie
