require(pacman)  # Gives a confirmation message.
pacman::p_load(pacman, seqinr, here, Biostrings, universalmotif)
library(universalmotif)

#Get the file paths to sequences
fly_file <- here("sequences", "X79493.fasta")
human_file <- here("sequences", "AY707088.fasta")

#Load fasta files into DNA-strings
fly_sequence <- readDNAStringSet(fly_file)
human_sequence <- readDNAStringSet(human_file)

#Define substitution matrix 
sub_mat <- nucleotideSubstitutionMatrix(match=1, mismatch = -1, baseOnly = TRUE)

#Make a local alignment 
local_alignment <- pairwiseAlignment(pattern = fly_sequence, 
                  subject = human_sequence,
                  type = "local",
                  substitutionMatrix = sub_mat,
                  gapOpening = 3,
                  gapExtension = 1)

#Make a global alignment
global_alignment <- pairwiseAlignment(pattern = fly_sequence, 
                                  subject = human_sequence,
                                  type = "global",
                                  substitutionMatrix = sub_mat,
                                  gapOpening = 3,
                                  gapExtension = 1)


#Generate 1000 randomized of same length as human and fly sequence
fly_random <- create_sequences(alphabet = "DNA", seqnum = 1000, seqlen = width(fly_sequence))
human_random <- create_sequences(alphabet = "DNA", seqnum = 1000, seqlen = width(human_sequence))

#Saves the score of the local and global alignments
local_random <- numeric(length(human_random)) #Saves the score of the local alignment
global_random <- numeric(length(human_random))

for (i in 1:length(human_random)){
  local_random[i] = pairwiseAlignment(pattern = fly_random[i], 
                                   subject = human_random[i],
                                   type = "local",
                                   substitutionMatrix = sub_mat,
                                   gapOpening = 3,
                                   gapExtension = 1,
                                   scoreOnly = TRUE)
  
  global_random[i] = pairwiseAlignment(pattern = fly_random[i], 
                                       subject = human_random[i],
                                       type = "global",
                                       substitutionMatrix = sub_mat,-
                                       gapOpening = 3,
                                       gapExtension = 1,
                                       scoreOnly = TRUE)
}

#Creates histograms of the scores of 
hist(local_random,
     main = "Local alignment scores of random sequences",
     xlab = "Score",
     ylab = "Number")
hist(global_random,
     main = "Global alignment scores of random sequences",
     xlab = "Score",
     ylab = "Number")

#Checks the probability of getting higher score than the global/local alignment
local_num_sign <- local_random[local_random >= score(local_alignment)]
local_pvalue <- local_num_sign/length(local_random)


global_num_sign <- global_random[global_random >= score(global_alignment)]
global_pvalue <- global_num_sign/length(global_random)
