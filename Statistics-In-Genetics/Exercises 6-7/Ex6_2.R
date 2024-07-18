require(pacman)  # Gives a confirmation message.
pacman::p_load(pacman, here, HMM, seqinr, BiocManager, msa)

#Load the gene files
MSA_env_file <- here("sequences", "Ex6_2", "MSA_env.fasta")
MSA_gag_file <- here("sequences", "Ex6_2", "MSA_gag.fasta")
MSA_pol_file <- here("sequences", "Ex6_2", "MSA_pol.fasta")

#Read the MSA files
MSA_env <- read.alignment(MSA_env_file, format = "fasta", forceToLower = FALSE)
MSA_gag <- read.alignment(MSA_gag_file, format = "fasta", forceToLower = FALSE)
MSA_pol <- read.alignment(MSA_pol_file, format = "fasta", forceToLower = FALSE)

#Calculate the Ka and Ks
env_kakas <- kaks(MSA_env)
gag_kakas <- kaks(MSA_gag)
pol_kakas <- kaks(MSA_pol)

#Calculate R
env_R <-env_kakas[["ka"]][1] / env_kakas[["ks"]][1]



gag_R <-gag_kakas[["ka"]][1] / gag_kakas[["ks"]][1]


pol_R <-pol_kakas[["ka"]][1] / pol_kakas[["ks"]][1]


