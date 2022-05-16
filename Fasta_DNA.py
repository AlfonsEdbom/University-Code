from os import path

from Trie import Trie

class Fasta_DNA:
    forward_strand: str
    reverse_strand: str

    def __init__(self, fasta_file) -> None:
        self.forward_strand = self.read_fasta(fasta_file)
        self.reverse_strand = self.calculate_reverse_DNA(self.forward_strand)

    def read_fasta(self, file_name: str) -> str:
        # Reads the fasta file
        sequence_dir = path.join(path.dirname(__file__), "sequences")
        file_path = path.join(sequence_dir, file_name)
        with open(file_path, 'r') as f:
            content = f.readlines()

        # Create string of DNA
        self.forward_strand = ""
        for i in range(1, len(content)):
            self.forward_strand += content[i].strip()

        return self.forward_strand

    def calculate_reverse_DNA(self, DNA_string: str) -> str:
        # Loop over DNA string from behind to create complimentary strand
        reversed_DNA = []
        for i in reversed(DNA_string):  # Match with correct opposing base
            if i == "A":
                reversed_DNA.append("T")
            elif i == "T":
                reversed_DNA.append("A")
            elif i == "G":
                reversed_DNA.append("C")
            elif i == "C":
                reversed_DNA.append("G")

        self.reverse_strand = "".join(reversed_DNA)

        return self.reverse_strand

    def get_forward_strand(self):
        return self.forward_strand

    def get_reverse_strand(self):
        return self.reverse_strand

    def build_primer_Trie(self, primer_length: int):

        t = Trie()
        forward_list = [self.forward_strand[i:i + primer_length]
                        for i in range(0, len(self.forward_strand)-primer_length+1)]
        reverse_list = [self.reverse_strand[i:i + primer_length]
                        for i in range(0, len(self.reverse_strand)-primer_length+1)]

        for i in forward_list:
            t.insert(i)

        for i in reverse_list:
            t.insert(i)

        return t
