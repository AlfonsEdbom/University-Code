require(pacman)  # Gives a confirmation message.
pacman::p_load(pacman, here, HMM, seqinr, BiocManager, msa)


#load the MSA files (gotten from jalview)
MSA_CYTB_file <- here("sequences", "Ex6_1", "MSA_CYTB.fasta")
MSA_ND1_file <- here("sequences", "Ex6_1","MSA_ND1.fasta")
MSA_ND2_file <- here("sequences", "Ex6_1", "MSA_ND2.fasta")

#Create alignment object
MSA_CYTB <- read.alignment(MSA_CYTB_file, format = "fasta", forceToLower = FALSE)
MSA_ND1 <- read.alignment(MSA_ND1_file, format = "fasta", forceToLower = FALSE)
MSA_ND2 <- read.alignment(MSA_ND2_file, format = "fasta", forceToLower = FALSE)

#Calculate the ka and ks
CYTB_kakas <- kaks(MSA_CYTB)
ND1_kakas <- kaks(MSA_ND1)
ND2_kakas <- kaks(MSA_ND2)

#Calculate the ratio R (ka/ks)
R1 <- numeric(3)
for (i in 1:3) {
  R1[i] <-CYTB_kakas[["ka"]][i] / CYTB_kakas[["ks"]][i]
}

R2 <- numeric(3)
for (i in 1:3) {
  R2[i] <-ND1_kakas[["ka"]][i] / ND1_kakas[["ks"]][i]
}

R3 <- numeric(3)
for (i in 1:3) {
  R3[i] <-ND2_kakas[["ka"]][i] / ND2_kakas[["ks"]][i]
}
