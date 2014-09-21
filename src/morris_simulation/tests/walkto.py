#!/usr/bin/python

from naoqi import ALProxy

try:
    motionProxy = ALProxy("ALMotion", '127.0.0.1', 9559)
except Exception, e:
    print "Could not create proxy"
    
try:
    postureProxy = ALProxy("ALRobotPosture", '127.0.0.1', 9559)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e
    
motionProxy.setSmartStiffnessEnabled(True)
postureProxy.goToPosture("StandInit", 4) 
        
x = .05
y = 0
t = 0
while True:
    motionProxy.moveTo(x, y, t, [["MaxStepFrequency", .8], ["TorsoWy", .122], ["MaxStepX", 0.2]])
