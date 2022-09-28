# Task 1 
rm(list = ls())

data = read.table(gzfile("zip.train"))
data <- as.matrix(data)

Four <- data[which(data[,1]==4),2:257]

colors <- c('white','black'); 
cus_col <- colorRampPalette(colors=colors)

par(mfrow= c(4,6))
par(mar=c(1, 1, 1, 1))

for (i in 1:24) {
  z <- matrix(Four[i,256:1],16,16,byrow=T)[,16:1]
  image(t(z), col=cus_col(256))
}


# Task 2
S = cov(Four)

eigen_dec = eigen(S)
par(mfrow=c(2, 2))
for (i in 1:4){
  p_vec = eigen_dec$vectors[, i]
  p_matrix = matrix(p_vec[256:1], 16, 16, byrow=T)[,16:1]
  image(t(p_matrix), col=cus_col(256))
}

par(mfrow=c(2, 2))
for (i in 253:256) {
  p_vec = eigen_dec$vectors[, i]
  p_matrix = matrix(p_vec[256:1], 16, 16, byrow=T)[,16:1]
  image(t(p_matrix), col=cus_col(256))
}



# Task 3

get_approx = function(obs, n, e_mat) {
  approximation = 0 
  for (i in 1:n) {
    yi = t(obs) %*% e_mat$vectors[, i]
    pcomp = yi %*% e_mat$vectors[, i]
    approximation = approximation + pcomp
  }
  return(approximation)
}


par(mfrow=c(2,3))
par(mar=c(1,1,1,1))
z <- matrix(Four[1,256:1],16,16,byrow=T)[,16:1]
image(t(z), col=cus_col(256))

for (i in c(30, 60, 100, 150, 200)) {
  approximation = get_approx(Four[1, ], i , eigen_dec)
  approx_mat = matrix(approximation[256:1], 16, 16, byrow=T)[,16:1]
  image(t(approx_mat), col=cus_col(256))
  print((norm(t(t(Four[1, ])) - t(approximation))^2)/256)
}

# Task 4 
variation = 0
i = 1

while (variation < 0.85) {
  total_variation = sum(eigen_dec$values)
  
  curr_variation = sum(eigen_dec$values[1:i])
  variation = curr_variation/total_variation
  
  i = i + 1
}

num_pcomps = i - 1
num_pcomps





# Task 5
Five_Six <- data[which(data[,1]==5 | data[,1] == 6),2:257]
Five_Six_w_labels <- data[which(data[,1]==5 | data[,1] == 6),1:257]

n = dim(Five_Six)[1] # sample size
set.seed(2022)
id = sample(1:n, floor(0.8*n)) 
train_data = Five_Six[id, ] # training set
test_data = Five_Six[-id, ] # testing set


S = cov(train_data) # training covariance matrix
mu = colMeans(train_data) # mean vector

# eigen decomposition of covariance matrix
eigen_dec = eigen(S) 
eigen_val = eigen_dec$values
eigen_vec = eigen_dec$vectors


# Get the first 2 principal components for train data
PC1 = numeric(length(train_data[, 1]))
PC2 = numeric(length(train_data[, 1]))

for (i in 1:length(train_data[, 1])){
  z1 = t(train_data[i, ] - mu) %*% eigen_vec[, 1]
  z2 = t(train_data[i, ] - mu) %*% eigen_vec[, 2]
  
  PC1[i] = z1
  PC2[i] = z2
}


# create new dataframe with labels and principal components for train data
train_labels = Five_Six_w_labels[id, 1]
test_dat = data.frame(train_labels, PC1, PC2)

# separate 5s and 6s
train_fives = test_dat[which(test_dat[,1]==5),2:3]
train_sixs = test_dat[which(dat[,1]==6),2:3]

# Get statistics for 5s and 6s
mu5 = colMeans(train_fives)
S5 = cov(train_fives)

colnames(S5)<-NULL
rownames(S5)<-NULL

mu6 = colMeans(train_sixs)
S6 = cov(train_sixs)

colnames(S6)<-NULL
rownames(S6)<-NULL


# Get test data

test_mu = colMeans(test_data)

test_PC1 = numeric(length(test_data[, 1]))
test_PC2 = numeric(length(test_data[, 1]))

for (i in 1:length(test_data[, 1])) {
  z1 = t(test_data[i, ]- test_mu) %*% eigen_vec[, 1]
  z2 = t(test_data[i, ]- test_mu) %*% eigen_vec[, 2]
  
  test_PC1[i] = z1
  test_PC2[i] = z2
}

test_labels = Five_Six_w_labels[-id, 1]

test_dat = data.frame(test_labels, test_PC1, test_PC2)


# classifier functions
exponent = function(my_vector, row_observation, cov_matrix){
  x = as.vector(row_observation) - as.vector(my_vector)
  result = exp(-t(t(x)) %*% solve(cov_matrix) %*% t(x)/2)
  return(result)
}

# The base/quota of the multinomial distribution
base = function(cov_matrix, p){
  result <- 1/(((2*pi)^(p/2))*sqrt(det(cov_matrix)))
  return(result)
}
# classify an observation as malignant=1, benign = 0
classifier <- function(row_observation, five_prob, six_prob){
  five <- base(S5, length(row_observation)) * exponent(mu5, row_observation, S5) * five_prob
  six <- base(S6, length(row_observation)) * exponent(mu6, row_observation, S6) * six_prob
  if (six > five){
    prediction <- 6
  } else{
    prediction <- 5
  }
  return(prediction)
}

five_prob = length(train_fives[,1]) / length(train_data[, 1]) 
six_prob = length(train_sixs[,1]) / length(train_data[, 1])
  

row_observation = test_dat[3, 2:3]
classifier(row_observation, five_prob, six_prob) # return 5 or 6


num_five = 0
num_six = 0
pred_col <- c()
for (i in 1:nrow(test_dat)) {
  guess <- classifier(test_dat[i, 2:3], five_prob, six_prob) # return 5 or 6
  if(guess == 5){ # guess is 1=malignant
    num_five = num_five + 1
    pred_col <- append(pred_col, 5)
  }else{ # guess is 0=benign
    num_six = num_six + 1
    pred_col <- append(pred_col, 6)
  }
}

# Print number of malignant and benign in test data
print(num_malignant)
print(num_benign)

# Calculate the classifier accuracy
cor_pred <- 0
wr_pred <- 0
for (i in 1:length(pred_col)){
  if(pred_col[i]==5 & test_dat[i,1]==5){ # if predict = 1 and diagnosis = "M"
    cor_pred <- cor_pred + 1
  }
  if(pred_col[i]==6 & test_data[i,1]==6){ # if predict = 0 and diagnosis = "B"
    cor_pred <- cor_pred + 1
  }
}

cor_pred
wr_pred














































