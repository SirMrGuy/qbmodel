logitdata <- read.csv('logit.csv')
l <- glm(win ~ diff, data = logitdata, family = 'binomial')
x <- seq(-10,80,1)
plot(x,1/(1+2.71828^-(x*l[['coefficients']][['diff']])),
     main='Win Probability vs. aPPB Difference',
     xlab='Score Difference',
     xlim=c(0,10),
     ylab='Win Probability',
     ylim=c(0,1),
     type='l',
     col='blue',
     lwd=2)
points(logitdata[['diff']],logitdata[['win']],
       pch=19,
       cex=1,
       col=rgb(red = 1, green = 0, blue = 0, alpha = 50/dim(logitdata)[1]))
summary(l)
