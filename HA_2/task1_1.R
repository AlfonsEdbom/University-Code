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
id = sample(1:n, floor(0.8*n)) 
train_data = Five_Six[id, ] # training set
test_data = Five_Six[-id, ] # testing set


S = cov(train_data)
means = colMeans(train_data)

eigen_dec = eigen(S)
eigen_val = eigen_dec$values
eigen_vec = eigen_dec$vectors

z1 = t(train_data[1, ]-means) %*% eigen_vec[, 1]
z2 = t(train_data[1, ]-means) %*% eigen_vec[, 2]

pcomp1 = z1 %*% eigen_vec[, 1]
pcomp2 = z2 %*% eigen_vec[, 2]


# predict test data??

z1_p = t(test_data[15, ]-means) %*% eigen_vec[, 1]
z2_p = t(test_data[15, ]-means) %*% eigen_vec[, 2]

pcomp1_p = z1_p %*% eigen_vec[, 1]
pcomp2_p = z2_p %*% eigen_vec[, 2]
