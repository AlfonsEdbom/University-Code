require(pacman)  # Gives a confirmation message.
pacman::p_load(pacman, seqinr, here, Biostrings, universalmotif, DECIPHER, GenomicRanges)


MSA_file <- here("sequences", "MSA.fasta")


#Read the file
MSA <- read.alignment(MSA_file, format = "fasta", forceToLower = FALSE)


dist_mat <- dist.alignment(MSA)


