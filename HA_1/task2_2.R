# read the data sets
train_data = read.table("Train.txt", sep=",") 
test_data = read.table("Test.txt", sep=",")

# separate malignant and benign
malignant = as.matrix(train_data[which(train_data[,1] == "M"), -1])
malignant = matrix(as.numeric(malignant), ncol = ncol(malignant))

benign = as.matrix(train_data[which(train_data[,1] == "B"), -1])
benign = matrix(as.numeric(benign), ncol = ncol(benign))

# Convert test data to matrix
test_data1 = as.matrix(test_data[-1,-1]) # Does not have first row or diagnosis
test_data1 = matrix(as.numeric(test_data1), ncol = ncol(test_data1))

# my vector for malignant and benign
my_malignant = colMeans(malignant)
my_benign = colMeans(benign)

# covariance matrix for malignant and benign
cov_malignant = cov(as.matrix(malignant))
cov_benign = cov(as.matrix(benign))

##################################################################
################### FUNCTIONS ####################################
##################################################################

# Exponential part of the multinomial distribution
exponent = function(my_vector, row_observation, cov_matrix){
  x = as.vector(row_observation) - as.vector(my_vector)
  result = exp(-t(x) %*% solve(cov_matrix) %*% t(t(x))/2)
  return(result)
}

# The base/quota of the multinomial distribution
base = function(cov_matrix, p){
  result <- 1/(((2*pi)^(p/2))*sqrt(det(cov_matrix)))
  return(result)
}
# classify an observation as malignant=1, benign = 0
classifier <- function(row_observation, M_prob, B_prob){
  M <- base(cov_malignant, length(row_observation)) * exponent(my_malignant, row_observation, cov_malignant) * M_prob
  B <- base(cov_benign, length(row_observation)) * exponent(my_benign, row_observation, cov_benign) * B_prob
  if (M > B){
    prediction <- 1
  } else{
    prediction <- 0
  }
  return(prediction)
}

##################################################################
################### END OF FUNCTIONS #############################
##################################################################

# Probabilities for being malignant or benign
M_prob = length(which(train_data[ , 1] == "M")) / (length(train_data[, 1])-1)
B_prob = length(which(train_data[ , 1] == "B")) / (length(train_data[, 1])-1)


# For each row in test data get classifier prediction
num_malignant = 0
num_benign = 0
pred_col <- c()
for (patient in 1:nrow(test_data1)) {
  guess <- classifier(test_data1[patient, ], M_prob, B_prob) # return 1 or 0
  if(guess == 1){ # guess is 1=malignant
    num_malignant = num_malignant + 1
    pred_col <- append(pred_col, 1)
  }else{ # guess is 0=benign
    num_benign = num_benign + 1
    pred_col <- append(pred_col, 0)
  }
}

# Print number of malignant and benign in test data
print(num_malignant)
print(num_benign)

# Calculate the classifier accuracy
cor_pred <- 0
wr_pred <- 0
for (i in 1:length(pred_col)){
  if(pred_col[i]==1 & test_data[i+1,1]=="M"){ # if predict = 1 and diagnosis = "M"
    cor_pred <- cor_pred + 1
  }
  if(pred_col[i]==0 & test_data[i+1,1]=="B"){ # if predict = 0 and diagnosis = "B"
    cor_pred <- cor_pred + 1
  }
}

accuracy <- cor_pred/length(pred_col)
accuracy

# Sanity test
nrow(test_data[which(test_data[,1] == "M"),])
num_malignant

nrow(test_data[which(test_data[,1] == "B"),])
num_benign
