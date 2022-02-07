#installing and activating packages
require(pacman)  # Gives a confirmation message.
pacman::p_load(pacman, seqinr, here, ORFik)

#Loads all the fasta files containing mitochondrial DNA
human_file <- here("sequences", "NC_001807.fasta")
chimp_file <- here("sequences", "NC_001643.fasta")
mouse_file <- here("sequences", "NC_005089.fasta")

#Defines a function that gets the ORFS in a fasta file with the minimum length of minumum_length
mito_orfs <- function(fasta_file, minimum_length) {
  start_codons <- startDefinition(3) #Defines start codons as ATA or ATG only (Appropriate for vertebrate mitochondrial DNA)
  stop_codons <- stopDefinition(2) #Defines stop codons as TAA, TAG, AGA or AGG (Same as above)
  
  orfs <- findORFsFasta(fasta_file, 
                        startCodon = start_codons,
                        stopCodon = stop_codons,
                        longestORF = TRUE,
                        minimumLength = minimum_length)
  
  return (orfs) }



#Human plots and calculations
all_human_orfs <- mito_orfs(human_file, 0) #Gets all human ORFS
potential_human_genes <- mito_orfs(human_file, 40) #Gets potential human genes

all_human_lengths <- width(ranges(all_human_orfs)) #Gets the lengths of all ORFS
potential_human_lengths <- width(ranges(potential_human_genes)) #Gets the lengths of potential genes 


hist(all_human_lengths,
     main = "All human ORF lengths",
     xlab = "ORF length",
     ylab = "Numer of ORFs")
hist(potential_human_lengths,
     main = "All potential human gene lengths",
     xlab = "ORF length",
     ylab = "Numer of ORFs")

human_sequence <- read.fasta(human_file, forceDNAtolower = FALSE, set.attributes = FALSE) #Read the human fasta file
human_sequence <- human_sequence[[1]]
human_sequence_length <- length(human_sequence)

sum(potential_human_lengths)/human_sequence_length


#Chimp plots and calculations
all_chimp_orfs <- mito_orfs(chimp_file, 0) #Gets all chimp ORFS
potential_chimp_genes <- mito_orfs(chimp_file, 40) #Gets potential human genes

all_chimp_lengths <- width(ranges(all_chimp_orfs)) #Gets the lengths of all ORFS
potential_chimp_lengths <- width(ranges(potential_chimp_genes)) #Gets the lengths of potential genes 

hist(all_chimp_lengths,
     main = "All chimp ORF lengths",
     xlab = "ORF length",
     ylab = "Numer of ORFs")
hist(potential_chimp_lengths,
     main = "All potential chimp gene lengths",
     xlab = "ORF length",
     ylab = "Numer of ORFs")

chimp_sequence <- read.fasta(chimp_file, forceDNAtolower = FALSE, set.attributes = FALSE) #Read the human fasta file
chimp_sequence <- chimp_sequence[[1]]
chimp_sequence_length <- length(chimp_sequence)

sum(potential_chimp_lengths)/chimp_sequence_length





#Mouse plots and calculations
all_mouse_orfs <- mito_orfs(mouse_file, 0) #Gets all human ORFS
potential_mouse_genes <- mito_orfs(mouse_file, 40) #Gets potential human genes

all_mouse_lengths <- width(ranges(all_mouse_orfs)) #Gets the lengths of all ORFS
potential_mouse_lengths <- width(ranges(potential_mouse_genes)) #Gets the lengths of potential genes 

hist(all_mouse_lengths,
     main = "All mouse ORF lengths",
     xlab = "ORF length",
     ylab = "Numer of ORFs")
hist(potential_mouse_lengths,
     main = "All potential mouse gene lengths",
     xlab = "ORF length",
     ylab = "Numer of ORFs")

mouse_sequence <- read.fasta(mouse_file, forceDNAtolower = FALSE, set.attributes = FALSE) #Read the human fasta file
mouse_sequence <- mouse_sequence[[1]]
mouse_sequence_length <- length(mouse_sequence)

sum(potential_mouse_lengths)/mouse_sequence_length


#Close packages and plots
p_unload(all) 
detach("package:datasets", unload = TRUE) 

# Clear console
cat("\014")  # ctrl+L
