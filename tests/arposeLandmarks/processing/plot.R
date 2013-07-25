library(ggplot2)

plotdata <- function(datafile, plotfile){
  d = read.table(datafile, header=T, quote="\"")
  summ <- summarySE(d, measurevar="estdistance", groupvars=c("knowndistance"))

  model <- summ[,"estdistance"] ~ summ[,"knowndistance"]
  png(plotfile)
  plot(model, col='blue', xlab="real distance (m)", ylab="estimated distance (m)", type="p")
  abline(lm(model), lty=5, col="red")
  x = summ[,"knowndistance"]
  y = summ[,"estdistance"]
  sd = summ[,"sd"]
  segments(x, y-sd,x, y+sd)
  epsilon = 0.01
  segments(x-epsilon,y-sd,x+epsilon,y-sd)
  segments(x-epsilon,y+sd,x+epsilon,y+sd)
  dev.off()
}

plotdata("straight.data", "straigth.plot")
plotdata("45degree.data", "45degree.plot")