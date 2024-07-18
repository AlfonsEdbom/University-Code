require(pacman)  # Gives a confirmation message.
pacman::p_load(pacman, seqinr, here, Biostrings, universalmotif, DECIPHER, GenomicRanges)
library(universalmotif, DECIPHER)


cow_file_nuc <- here("sequences", "nuc_cow_homeo.fasta")
human_file_nuc <- here("sequences", "nuc_human_homeo.fasta")

cow_file_aa <- here("sequences", "cow_homeo.fasta")
human_file_aa <- here("sequences", "human_homeo.fasta")


nuc_sequences <- readDNAStringSet(c(cow_file_nuc, human_file_nuc))
aa_sequences <- readAAStringSet(c(cow_file_aa, human_file_aa))


nuc_sub_mat <- nucleotideSubstitutionMatrix(match=1, mismatch = -1, baseOnly = TRUE)
aa_sub_mat <- data("BLOSUM45")

nuc_PSA <- pairwiseAlignment(nuc_sequences[1], nuc_sequences[2],type="local", substitutionMatrix=nuc_sub_mat, gapOpening = 3,
                             gapExtension = 1)

aa_PSA <- pairwiseAlignment(aa_sequences[1], aa_sequences[2], type="local", substitutionMatrix=aa_sub_mat, gapOpening=3, gapExtension=1)

nuc_file <- here("sequences", "nucPSA.fasta")
writePairwiseAlignments(nuc_PSA, nuc_file)

aa_file <- here("sequences", "aaPSA.fasta")
writePairwiseAlignments(aa_PSA, aa_file)

seq1 <- c(alignedPattern(nuc_PSA), alignedSubject(nuc_PSA))
BrowseSeqs(seq1)

seq2 <- c(alignedPattern(aa_PSA), alignedSubject(aa_PSA))
BrowseSeqs(seq2)

