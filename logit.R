logitdata <- read.csv('logit2.csv')
l <- glm(win ~ diff, data = logitdata, family = 'binomial')
x <- seq(-80,80,1)
plot(x,1/(1+2.71828^-(x*l[['coefficients']][['diff']])),
     main='Win Probability vs. Groger Score Difference',
     xlab='Score Difference',
     ylab='Win Probability',
     type='l',
     col='blue',
     lwd=2)
points(logitdata[['diff']],logitdata[['win']],
       pch=19,
       cex=1,
       col=rgb(red = 1, green = 0, blue = 0, alpha = 60/dim(logitdata)[1]))
summary(l)
