#!/usr/bin/env python  
'''
Created on Feb 21, 2013

@author: mllofriu
'''
import rospy

from romina2.msg import PolygonsStamped
from visualization_msgs.msg import  Marker, MarkerArray
import message_filters
from morris_simulation.perception import AffordanceCalc
from rospy import Duration

class Affordances(object):
    floorFrame = "/l_sole"
    affCalc = AffordanceCalc()

    def __init__(self):
        sub = message_filters.Subscriber("/lines", PolygonsStamped)
        self.cache = message_filters.Cache(sub, 200)
        rospy.loginfo( "Affordances initiated")
    
    def getAffordances(self):
        data = self.cache.getElemBeforeTime(rospy.Time.now())

        if data != None:
            return self.affCalc.calcAffordances(data.polygons)
        else:
            return self.affCalc.calcAffordances([])
        
    
           
        
if __name__ == "__main__":
    rospy.init_node('affordancesCalculator')
    a = Affordances()
    rospy.sleep(1)
    while not rospy.is_shutdown():
        print a.getAffordances()
        rospy.sleep(1)
    exit()