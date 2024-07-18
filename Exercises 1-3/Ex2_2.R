require(pacman)  # Gives a confirmation message.
pacman::p_load(pacman, seqinr, here, ORFik, kebabs)


mito_orfs <- function(seqs, minimum_length) {
  start_codons <- startDefinition(3) #Defines start codons as ATA or ATG only (Appropriate for vertebrate mitochondrial DNA)
  stop_codons <- stopDefinition(2) #Defines stop codons as TAA, TAG, AGA or AGG (Same as above)
  
  orfs <- findORFs(seqs, 
                        startCodon = start_codons,
                        stopCodon = stop_codons,
                        longestORF = TRUE,
                        minimumLength = minimum_length)
  
  return (orfs) }

num_seqs <- 1000
seq_length <- 17000
random_seqs <- genRandBioSeqs("DNA", num_seqs, seq_length, biostring=FALSE, seed=1)

orfs <- mito_orfs(random_seqs, 40)
gr <- unlist(orfs)

max(width(gr))

hist(width(gr),
main = "ORF lengths of 1000 randomly generated sequences",
xlab = "ORF length",
ylab = "Numer of ORFs")

