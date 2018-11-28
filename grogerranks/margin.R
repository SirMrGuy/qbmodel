margindata <- read.csv('margin2.csv')
lin <- lm(margin ~ diff, data = margindata)
x <- seq(-80,80,1)
plot(x,lin[['coefficients']][['(Intercept)']]+x*lin[['coefficients']][['diff']],
     main='Margin vs. Groger Score Difference',
     xlab='Score Difference',
     xlim=c(0,70),
     ylab='Margin',
     ylim=c(-600,700),
     type='l',
     col='blue',
     lwd=2)
points(margindata[['diff']],margindata[['margin']],
       pch=19,
       cex=1,
       col=rgb(red = 1, green = 0, blue = 0, alpha = 100/dim(margindata)[1]))
abline(a=0, b=0)
summary(lin)