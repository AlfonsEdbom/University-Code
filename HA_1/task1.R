### --- 2.18 --- ###

avg = matrix(c(0.766, 0.508, 0.438, 0.161))

data = c(0.856, 0.635, 0.173, 0.096, 0.635, 0.568, 0.128, 0.067, 0.173, 0.127, 0.171, 0.039, 0.096, 0.067, 0.039, 0.043)
variance = matrix(data=data, nrow=4, byrow=TRUE)


## a) ##
# Get the average total energy consumption
c1 = c(1, 1, 1, 1) # Want to get energy consumption from all variables

tot_avg = c1 %*% avg 


tot_var = t(c1)%*%variance%*%t(t(c1))


### b) ###
c2 = matrix(c(1, 1, 1, 1, 1, -1, 0, 0), ncol = 2, byrow=FALSE)

z_average = mean(t(c2) %*% avg)
Sz = t(c2) %*% variance %*% t(t(c2))




### --- 3.32 --- ###

x_avg = matrix(c(2.4, -1,3, 0), nrow=1)

data = c(4, -1, 0.5, -0.5, 0,
         -1, 3, 1, -1, 0, 
         0.5, 1, 6, 1, -1,
         0, 0, -1, 0, 2)

S = matrix(data= data, ncol=5, byrow=TRUE)

A = matrix(c(1, -1, 1, 1), nrow=2, byrow=TRUE)
B = matrix(c(1, 1, 1, 1, 1, -2), nrow=2, byrow=TRUE)

X1 = matrix(c(2, 4), nrow=2)
X2 = matrix(c(-1, 3, 0), nrow=3)

## a) ##

X1

## b) ##

E = A %*% X1
X1

## c) ##

S = matrix(c(4, -1, -1, 3), byrow=TRUE, nrow = 2)
S
## d) ##

S2 = A %*% S %*% t(A) 

## e) ##

X2

## f) ##

S3 = B %*% X2

## g) ##

S4 = matrix(c(6, 1, -1, 1, 4, 0, -1, 0, 2), byrow=TRUE, nrow=3)
S4

## h) ##

S5 = B %*% S4 %*% t(B)
S5

## i) ##

S6 = matrix(c(0.5, -0.5, 0, 1, -1, 0), )
S6

## j) ##

S7 = A %*% S6 %*% t(B)
S7


### 4.16 ###

## a) ##

c1 = matrix(c(0.25, -0.25, 0.25, -0.25))
my_1 = sum(c1)
sigma_1 = sum(c1^2)


c2 = matrix(c(0.25, 0.25, -0.25, -0.25))
my_2 = sum(c2)
sigma_2 = sum(c2^2)

## b) ##
????????????????????????
