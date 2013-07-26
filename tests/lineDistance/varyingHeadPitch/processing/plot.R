plotdata <- function(datafile, plotfile){
  d = read.table(datafile, header=T, quote="\"")
  names(d) = c('headPitch', 'estdistance')
  summ <- summarySE(d, measurevar="estdistance", groupvars=c("headPitch"))

  model <- summ[,"estdistance"] ~ summ[,"headPitch"]
  png(plotfile)
  plot(model, data=d, col='blue',
       xlab="head pitch (degrees)",
       ylab="estimated distance (m)", type="p", ylim=c(0.2,.6))
  abline(lm(model), lty=5, col="red")
  x = summ[,"headPitch"]
  y = summ[,"estdistance"]
  sd = summ[,"sd"]
  segments(x, y-sd,x, y+sd)
  epsilon = 0.2
  segments(x-epsilon,y-sd,x+epsilon,y-sd)
  segments(x-epsilon,y+sd,x+epsilon,y+sd)
  dev.off()
}

plotdata('distanceData.data', 'lineDistancePitch.plot')