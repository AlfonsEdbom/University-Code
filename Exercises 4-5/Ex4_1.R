require(pacman)  # Gives a confirmation message.
pacman::p_load(pacman, here, Biostrings, HMM)

#Get the path to the FASTA file
virus_file <- here("sequences", "NC_001416.fasta")

#load the file
virus_seq <- read.fasta(virus_file)


HMM_2state <- initHMM(c("H_GC", "H_AT"), c("A", "T", "C", "G"), )

simHMM(HMM_2state, 100)

viterbiTraining(HMM_2state, obs)

obs <- toString(virus_seq)



#Close packages and plots
p_unload(all) 
detach("package:datasets", unload = TRUE) 

# Clear console
cat("\014")  # ctrl+L