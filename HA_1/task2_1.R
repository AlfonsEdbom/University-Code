rm(list=ls())

install.packages("MVN")
library(bootstrap, MVN)

data(scor)

str(scor) # structure of scor
summary(scor) # summary of each variable
#tail(scor) ; head(scor)


# multivariate normal assumption tests
# Check all and determine using the consensus from all tests
mvn(data=scor, mvnTest = "mardia")
mvn(data=scor, mvnTest = "hz")
mvn(data=scor, mvnTest = "royston")
mvn(data=scor, mvnTest = "dh")
mvn(data=scor, mvnTest = "energy")

# Chi-square Q-Q plot. 
# Compare the observed dis. with the hypothesized, want observations to follow line
mvn(data=scor, multivariatePlot = "qq")

# Univariate plots and tests

## Univariate plots
mvn(data=scor, univariatePlot = "qqplot")
mvn(data=scor, univariatePlot = "histogram")
mvn(data=scor, univariatePlot = "box")
mvn(data=scor, univariatePlot = "scatter")

## Univariate tests
mvn(data=scor, univariateTest = "SW") #shapiro-wilk test: max 5000, min 3 cases
mvn(data=scor, univariateTest = "CVM") # Cramer-von-Mises
mvn(data=scor, univariateTest = "Lillie") # Lilliefors test
mvn(data=scor, univariateTest = "SF") #Shapiro-Francia test
mvn(data=scor, univariateTest = "AD") # Anderson-Darling test


# Do some contour plot on the normally distributed variables
scor2 = scor[1:88, 2:3] # only contain vec and alg columns

mvn(data=scor2, multivariatePlot="persp") # perspective plot
mvn(data=scor2,multivariatePlot = "contour")

# Detecting outliers
mvn(data=scor, multivariateOutlierMethod="quan") #quantile method based on mahalanobis distance
mvn(data=scor, multivariateOutlierMethod="adj") #adjusted quantile method

#using only subset of data
mvn(data=scor, subset="vec", mvnTest="hz") # Does not work???????????????
