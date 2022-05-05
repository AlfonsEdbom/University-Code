def calc_anneal_temp(sequence: str) -> float:
    anneal_temp = 0

    for base in sequence:
        if base in ["A", "T"]:
            anneal_temp += 2
        elif base in ["C", "G"]: # Needs to be elif, since other char are gaps
            anneal_temp += 4


    return anneal_temp

def get_GCC(sequence: str, max_GC: int, min_GC: int, winsize: int=20, step: int = 3):
    for i in range(0, len(sequence), step):
        for j in ["A", "T", "C", "G"]:

        num_G = count()
        num_AT = 0
        window = sequence[i:i+winsize]



class Filters:
    def __init__(self, sequences: list[str]):
        self.forward = sequences[0]
        self.reverse = sequences[1]

    def GC_content(self, max_GC, min_GC):
        """Removes portions of genome that have too much/little GC-content"""
        for i in range(0, len(self.forward[0]), 3):
            window = self.sequences[0]






    def annealing_temp(self, max_T, min_T):
        """Only keep primers /w appropriate Anneal_temp """
        pass

    def GC_clamp(self):
        """Removes primers that do not have a GC clamp"""
        pass

    def GC_end(self):
        """Only keep primers /w appopriate GC content in the end"""
        # 3 out 5 last are GC


