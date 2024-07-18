require(pacman)  # Gives a confirmation message.
pacman::p_load(pacman, seqinr, here) 

#Get current path and get the path to the FASTA file
here <- here("sequences", "NC_001416.fasta")

#Read the fasta file and get only the sequence
virus <- read.fasta(here, forceDNAtolower = FALSE, set.attributes = FALSE) #Read the FASTA FILE
virusseq <- virus[[1]]

#Function taken from https://a-little-book-of-r-for-bioinformatics.readthedocs.io/en/latest/src/chapter2_answers.html
#Creates a sliding windows plot of with the size windowsize
slidingwindowplot <- function(windowsize, inputseq)
{
  starts <- seq(1, length(inputseq)-windowsize, by = windowsize)
  n <- length(starts)
  chunkGCs <- numeric(n)
  for (i in 1:n) {
    chunk <- inputseq[starts[i]:(starts[i]+windowsize-1)]
    chunkGC <- GC(chunk)
    chunkGCs[i] <- chunkGC
  }
  plot(starts,chunkGCs,
       type="b",
       xlab="Nucleotide start position",
       ylab="GC content")
}

#Calls slidingwindowplot at specified window size and creates a plot
slidingwindowplot(1000, virusseq)

#Close packages and plots
p_unload(all) 
detach("package:datasets", unload = TRUE) 

# Clear console
cat("\014")  # ctrl+L
