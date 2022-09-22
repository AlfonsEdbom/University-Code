# random sample from Hemnet don't use???
r_sample = c(6, 9, 3, 6, 6, 13, 1, 10, 5, 4)

## lambda (avg, on/off season)
lambda1 = 5
lambda2 = 7

# probability on/off season
pi1 = 0.5
pi2 = 0.5

# loop variables
min_diff = 0.0001

curr_lambda1_diff = 10
curr_lambda2_diff = 10
i = 0


while ((curr_lambda1_diff > min_diff) &(curr_lambda2_diff > min_diff)) {
  i = i +1
  prob1 = ppois(r_sample, lambda1) * pi1
  prob2 = ppois(r_sample, lambda2) * pi2
  
  post_1 = prob1 / (prob1 + prob2)
  post_2 = prob2 / (prob1 + prob2)
  
  # update/ M-step
  lambda1_new = mean(post_1*r_sample)
  lambda2_new = mean(post_2*r_sample)
  
  pi1_new = mean(post_1)
  pi2_new = mean(post_2)
  
  # Get difference for each variable
  curr_lambda1_diff = abs(lambda1_new-lambda2)
  curr_lambda2_diff = abs(lambda2_new-lambda2)
  
  curr_pi1_diff = abs(pi1_new-pi1)
  curr_pi2_diff = abs(pi2_new-pi2)
  
  # set new variable to just normal/previous
  lambda1 = lambda1_new
  lambda2 = lambda2_new
  
  pi1 = pi1_new
  pi2 = pi2_new
  
}

i

lambda1_new
pi1_new

lambda2_new
pi2_new
