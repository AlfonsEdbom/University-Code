require(pacman)  # Gives a confirmation message.
pacman::p_load(pacman, here, HMM, seqinr, BiocManager, msa, phylogram, ape, dndextend)

#Get the file path to the MSA file
MSA_file <- here("sequences", "Ex7_1", "MSA_mito.fasta")

#Read the file
MSA <- read.alignment(MSA_file, format = "fasta", forceToLower = FALSE)

#Calculate the distance matrix for all the sequences
dist_mat <- dist.alignment(MSA)

#Include the Jukes Cantor correlation for each of the distances
JC_corr <- dist_mat
for (i in 1: length(JC_corr)) {
  JC <- (-0.75*log(1-(4/3)*JC_corr[i]))
  JC_corr[i] = JC
}

#Build neighbour-joining trees
phy1 <- nj(JC_corr)
phy2 <- nj(dist_mat)

#Set the root to Gibbon (known beforehand this is the outgroup)
phy1 <- root(phy1, "Gibbon")
phy2 <- root(phy2, "Gibbon")

#Convert phylo object to dendogram to be able to plot
dnd1 <- as.dendrogram(phy1)
dnd2 <- as.dendrogram(phy2)

#Make into ladder
dnd1 <- ladder(dnd1)
dnd2 <- ladder(dnd2)

#Plot the trees
plot(dnd1, )
plot(dnd2)

