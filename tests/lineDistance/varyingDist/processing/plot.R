plotdata <- function(datafile, plotfile){
  d = read.table(datafile, header=T, quote="\"")
  names(d) = c('knowndistance', 'estdistance')
  summ <- summarySE(d, measurevar="estdistance", groupvars=c("knowndistance"))

  model <- summ[,"estdistance"] ~ summ[,"knowndistance"]
  png(plotfile)
  plot(model, col='blue', xlab="real distance (m)", ylab="estimated distance (m)", type="p",ylim=c(0,1), xlim=c(0,1), cex.lab=1.5, cex.axis=1.5)
  abline(lm(model), lty=5, col="red")
  abline(coef=c(0,1), lty=5, col="blue")
  x = summ[,"knowndistance"]
  y = summ[,"estdistance"]
  sd = summ[,"sd"]
  segments(x, y-sd,x, y+sd)
  epsilon = 0.01
  segments(x-epsilon,y-sd,x+epsilon,y-sd)
  segments(x-epsilon,y+sd,x+epsilon,y+sd)
  dev.off()
}

plotdata('distanceData.data', 'lineDistance.png')