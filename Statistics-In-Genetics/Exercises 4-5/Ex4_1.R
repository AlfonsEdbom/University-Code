require(pacman)  # Gives a confirmation message.
pacman::p_load(pacman, here, HMM, seqinr)

#Get path to the FASTA file
virus_file <- here("sequences", "NC_001416.fasta")

#load the file
virus_seq <- read.fasta(virus_file,forceDNAtolower = FALSE)

#The states

Symbols <- c("A", "T", "C", "G")

#Define parameters for 2 state - HMM
States <- c("H_GC", "H_AT")
start <- c(.5, .5) #probability to start in either state
trans <- matrix(c(.75, .25, .25, .75), 2) #probability to transition from a state to another
emission <- matrix(c(.05, .45, .05, .45, .45, .05, .45, .05), 2) #for each state, the probability to emit a given symbol

#Create 2 initial state HMM
HMM_2state <- initHMM(States, Symbols, startProbs = start, transProbs = trans, emissionProbs = emission)

#Simulate sequence of length 100 with HMM
simHMM(HMM_2state, 100)

#Train HMM to find optimal parameter settings
obs <- unlist(getSequence(virus_seq))
HMM_2new <- baumWelch(HMM_2state, obs, 10, delta=1E-9)

#Create 4 state HMM
States <- c("H_G", "H_C","H_A", "H_T")
Symbols <- c("G", "C", "A", "T")
start <- c(.25, .25, .25, .25)
trans <- matrix(c(.8, .1, .05, .05, .1, .8, .05, .05, .05, .05, .8, .1, .05, .05, .1, .8), 4)
emission <- matrix(c(.8, .1, .05, .05, .1, .8, .05, .05, .05, .05, .8, .1, .05, .05, .1, .8), 4)

#Create HNMM
HMM_4state <- initHMM(States, Symbols, startProbs = start, transProbs = trans, emissionProbs = emission)

#Simulate sequence of length 100 with HMM
simHMM(HMM_4state, 100)

#Train HMM to find optimal parameter settings
obs <- unlist(getSequence(virus_seq))
HMM_4new <- baumWelch(HMM_4state, obs, 10, delta=1E-9)
