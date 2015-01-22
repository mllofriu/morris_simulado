#!/usr/bin/env python  
'''
Created on Feb 21, 2013

@author: mllofriu
'''
import rospy

from romina2.msg import PolygonsStamped
import message_filters
from morris_simulation.perception import AffordanceCalc
from morris_simulation.msg import Affordances
from rospy import Duration

class AffordancePublisher(object):
    floorFrame = "/l_sole"
    affCalc = AffordanceCalc()

    def __init__(self):
        self.sub = rospy.Subscriber("/lines", PolygonsStamped, self.publishAffordances)
        self.pub = rospy.Publisher("/affordances", Affordances, queue_size=10)
        rospy.loginfo( "Affordances initiated")
    
    def publishAffordances(self, linesMsg):
        affMsg = Affordances()
        affMsg.header.stamp = linesMsg.header.stamp
        
        if linesMsg.polygons != None:
            affMsg.affordances = self.affCalc.calcAffordances(linesMsg.polygons)
        else:
            affMsg.affordances = self.affCalc.calcAffordances([])
        
        self.pub.publish(affMsg);
        
           
        
if __name__ == "__main__":
    rospy.init_node('affordancesCalculator')
    a = AffordancePublisher()
    rospy.spin()