require(pacman)  # Gives a confirmation message.
pacman::p_load(pacman, seqinr, here, ORFik, kebabs)

virus_file <- here("sequences", "NC_000907.fasta")



mito_orfs <- function(fasta_file, minimum_length) {
  start_codons <- startDefinition(3) #Defines start codons as ATA or ATG only (Appropriate for vertebrate mitochondrial DNA)
  stop_codons <- stopDefinition(2) #Defines stop codons as TAA, TAG, AGA or AGG (Same as above)
  
  orfs <- findORFsFasta(fasta_file, 
                        startCodon = start_codons,
                        stopCodon = stop_codons,
                        longestORF = TRUE,
                        minimumLength = minimum_length)
  
  return (orfs) }


all_virus_orfs <- mito_orfs(virus_file, 0) #Gets all human ORFS


cutoffs <- seq(0, 150, by=10)
num_orfs <- numeric(length(cutoffs))
for (i in 1:length(cutoffs)) {
  potential_virus_genes <- mito_orfs(virus_file, cutoffs[i])
  num_orfs[i] = length(width(ranges(potential_virus_genes)))
}

plot(cutoffs, num_orfs, type="b", xlab= "Minimum length of ORF", ylab = "Number of ORFs found")

hist(width(ranges(all_virus_orfs)), xlim=c(0,600), breaks = 300, xlab= "Length of all ORFs found", ylab="Number of ORFs", main="")

