library(mixtools)

### a) ###

# average
mu = as.vector(c(2,3))

# given values for std. dev
sigma_1 = 1
sigma_2 = 2

# given value for correlation
corr = 0.7

# corr = sigma_12/ (sigma_1 * sigma_2)
sigma_12 = corr * sigma_1 * sigma_2

# covariance matrix
S = matrix(c(sigma_1^2, sigma_12, sigma_12, sigma_2^2), byrow=TRUE, nrow=2)

# generate 1000 obs. from multivariate normal distribution
obs = rmvnorm(1000, mu = mu, sigma = S)

# plot the variables against each other
plot(x=obs[, 1], y=obs[, 2], xlab = "X1", ylab = "X2")



### b) ###
# Get 1000 obs. from 1 bernoulli trail with p=0.6
bernoulli_obs = rbinom(n=1000,size=1, prob=0.6)

#Mu vectors, given
mu1 = as.vector(c(2, 3))
mu2 = as.vector(c(3, 2))

#S vectors, given corr. 0,5 for both S1, S2
S1 = matrix(c(0.2^2, 0.5*0.2*0.6, 0.5*0.2*0.6, 0.6^2), byrow=TRUE, nrow=2)
S2 = matrix(c(0.4^2, 0.5*0.4*0.3, 0.5*0.4*0.3, 0.3^2), byrow=TRUE, nrow=2)

# Get a random sample from either multivariate normal dist
# Depends on outcome of the bernoulli obs
# bernoulli=1 -> N1, bernoulli=0 -> N2
results = matrix(0, length(bernoulli_obs), 2)
for (i in 1:length(bernoulli_obs)){
  if (bernoulli_obs[i] == 1) {
    random_sample1 = rmvnorm(1, mu=mu1, sigma=S1)
    results[i, 1] = random_sample1[1, 1]
    results[i, 2] = random_sample1[1, 2]
  } else{
    random_sample2 = rmvnorm(1, mu=mu2, sigma=S2)
    results[i, 1] = random_sample2[1, 1]
    results[i, 2] = random_sample2[1, 2]
  }
}

#plot the results
plot(results)

### c) ###

# Test different parameters and see if we get similar results as the start
lambda= c(0.70, 0.30)
means = list(as.vector(c(1, 5)), as.vector(c(6, 2)))
sigmas = list(matrix(c(0.1, 0.01, 0.01, 0.4), byrow=TRUE, nrow=2), 
              matrix(c(0.2, 0.005, 0.005, 0.1), byrow=TRUE, nrow=2))

epsilon = 1e-05 # Stop criterion

out = mvnormalmixEM(results, mu=means ,sigma = sigmas, 
                    lambda = lambda, epsilon = epsilon)
out[2:4]
