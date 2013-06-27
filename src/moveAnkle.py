#!/usr/bin/env python 
'''
Created on May 28, 2013

@author: mllofriu
'''

import roslib; roslib.load_manifest('morris_simulation')
import rospy
from moveJoint import JointMover
from naoqi import ALProxy

if __name__ == '__main__':
    rospy.init_node("move ankle")
    ankle = "LAnklePitch"
    time = 1
    # Enable stiffness
    try:
        motionProxy = ALProxy("ALMotion", "127.0.0.1", 9559)
        motionProxy.wakeUp()
        jm = JointMover()
        rospy.loginfo("Going to starting position")
        jm.move(ankle, [0.922747], [10])
        motionProxy.rest()
        rospy.sleep(time)
        motionProxy.wakeUp()
        rospy.loginfo("At Starting position")
        for i in range(3):
            rospy.loginfo("Going to other end")
            jm.move(ankle, [-1.189516], [time])
            rospy.loginfo("At the other end")
            motionProxy.rest()
            rospy.sleep(time)
            motionProxy.wakeUp()
            rospy.loginfo("Going to starting position again")
            jm.move(ankle, [0.922747], [time])
            rospy.loginfo("At the starting position again")
            motionProxy.rest()
            rospy.sleep(time)
            motionProxy.wakeUp()
        motionProxy.rest()
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e
            

    