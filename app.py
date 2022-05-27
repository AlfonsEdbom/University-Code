from tkinter import *
from tkinter import ttk, filedialog, Canvas

from Fasta_DNA import Fasta_DNA
from Candidate_Primers import Candidate_Primers
from Primer_Pairs import Primer_Pairs

class GUI:
    def __init__(self, root):
        root.title("PCR Primer Finder")

        # Create the frames
        settings_frame = ttk.LabelFrame(root, padding=(3, 3, 12, 12))
        # Create settings widgets

        ## File related widgets
        file_label = ttk.Label(settings_frame, text="Load a Fasta File:")
        self.fasta_file = StringVar()
        file_button = ttk.Button(settings_frame, text="Open file", command=self.open_file)

        file_name = ttk.Label(settings_frame, textvariable=self.fasta_file)

        ## Settings related widgets
        ### Primer length
        primer_length_label = ttk.Label(settings_frame, text="Primer length: ")
        self.primer_length = StringVar()
        length_box = ttk.Entry(settings_frame, textvariable=self.primer_length)
        length_box.insert(0, "20")

        ### GC content
        min_GC_label = ttk.Label(settings_frame, text="Minimum GC content in primer: ")
        self.min_GC = StringVar()
        min_GC_box = ttk.Entry(settings_frame, textvariable=self.min_GC)
        min_GC_box.insert(0, "30")

        max_GC_label = ttk.Label(settings_frame, text="Maximum GC content in primer: ")
        self.max_GC = StringVar()
        max_GC_box = ttk.Entry(settings_frame, textvariable=self.max_GC)
        max_GC_box.insert(0, "80")

        ### Annealing temperature
        min_annealing_label = ttk.Label(settings_frame, text="Minimum annealing temperature for primer: ")
        self.min_annealing = StringVar()
        min_annealing_box = ttk.Entry(settings_frame, textvariable=self.min_annealing)
        min_annealing_box.insert(0, "58")

        max_annealing_label = ttk.Label(settings_frame, text="Maximum annealing temperature for primer: ")
        self.max_annealing = StringVar()
        max_annealing_box = ttk.Entry(settings_frame, textvariable=self.max_annealing)
        max_annealing_box.insert(0, "62")

        ### DeltaT
        min_deltaT_label = ttk.Label(settings_frame, text="Minimum difference in annealing temperature: ")
        self.min_deltaT = StringVar()
        min_deltaT_box = ttk.Entry(settings_frame, textvariable=self.min_deltaT)
        min_deltaT_box.insert(0, "15")

        ## Get primers
        get_primers = ttk.Button(settings_frame, text="Get Primers", command=self.get_primers)

        # Grid frames
        settings_frame.grid(column=0, row=0, sticky=(N, S, E, W))

        # Grid widgets
        file_label.grid(column=0, row=0)
        file_button.grid(column=1, row=0)
        file_name.grid(column=0, row=1)

        primer_length_label.grid(column=2, row=0)

        length_box.grid(column=3, row=0)

        min_GC_label.grid(column=2, row=1)
        min_GC_box.grid(column=3, row=1)

        max_GC_label.grid(column=4, row=1)
        max_GC_box.grid(column=5, row=1)

        min_annealing_label.grid(column=2, row=2)
        min_annealing_box.grid(column=3, row=2)

        max_annealing_label.grid(column=4, row=2)
        max_annealing_box.grid(column=5, row=2)

        min_deltaT_label.grid(column=2, row=3)
        min_deltaT_box.grid(column=3, row=3)

        get_primers.grid(column=4, row=3)
        # Resizing / column and row configurations
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

    def open_file(self, *args):
        filename = filedialog.askopenfilename(initialdir="../sequences", title="Select File",
                                              filetypes=(("Fasta files", "*.fasta"), ("All files", "*.*")))

        self.fasta_file.set(filename)

    def get_primers(self, *args):
        # Get settings
        primer_length = int(self.primer_length.get())
        GC_min = int(self.min_GC.get())
        GC_max = int(self.max_GC.get())
        T_min = int(self.min_annealing.get())
        T_max = int(self.max_annealing.get())
        deltaT = int(self.min_deltaT.get())
        GC_window = 30
        fasta_file = str(self.fasta_file.get())

        # Create DNA-object containing DNA in Fasta file
        genome_DNA = Fasta_DNA(fasta_file)

        # Build a trie containing all primers of specific length (f and r)
        t = genome_DNA.build_primer_Trie(primer_length)

        candidate_primers = Candidate_Primers(genome_DNA)  # initiate filter object
        candidate_primers.filter_GC_content(GC_window, GC_min, GC_max)  # remove windows with too high GC-content
        candidate_primers.apply_filters(primer_length, T_min, T_max)  # Apply the rest of the filteres
        candidate_primers.remove_non_unique(t)
        candidate_primers.remove_low_complexity_primers()
        candidate_primers.remove_similar(t, deltaT)  # Remove primers with too low deltaT

        PPs = Primer_Pairs(genome_DNA, candidate_primers.forward_primers, candidate_primers.reverse_primers)
        PPs.find_primer_pairs(300, 1500, is_circular=True)
        PPs.filter_primer_pairs(GC_min, GC_max)
        PPs.restriction_enzymes_cut()

        primer_pairs = PPs.get_primer_pairs()

        # Create new window
        result_window = Toplevel()
        result_window.title = "Primer pairs"

        listbox = Listbox(result_window, width=400, height=40)
        ver_scrollbar = ttk.Scrollbar(result_window, orient="vertical")


        for i, primer_pair in enumerate(primer_pairs):
            forward_primer, reverse_primer, contig_length, BAMHI, EcoRI, HINDIII, NotI, XbaI = primer_pair

            insert_string = f"Forward primer: {forward_primer} | Reverse primer: {reverse_primer} | Contig length: {contig_length} | BAMHI fragment lengths {BAMHI} | EcoRI fragment lengths {EcoRI} | HINDIII fragment lengths {HINDIII} | NotI fragment lengths {NotI} | XbaI fragment lengths {XbaI}"

            listbox.insert(i, insert_string)

        listbox.pack(side=LEFT, fill=BOTH)
        ver_scrollbar.pack(side=RIGHT, fill=BOTH)

        listbox.config(yscrollcommand=ver_scrollbar.set)
        ver_scrollbar.config(command=listbox.yview)


root = Tk()
GUI(root)

root.mainloop()
