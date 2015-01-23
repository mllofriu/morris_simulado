#!/usr/bin/env python  
'''
Created on May 22, 2013

@author: mllofriu
'''


import rospy


from visualization_msgs.msg import  Marker
import message_filters
from morris_simulation.msg import Affordances
from ar_pose.msg import ARMarkers

class InfoGatherer(object):
    '''
    classdocs
    '''

    def __init__(self):
        # Listen to visualization_markers for markers
        sub = message_filters.Subscriber("/ar_pose/ar_pose_marker", ARMarkers)
        self.markersCache = message_filters.Cache(sub, 10)
        sub = message_filters.Subscriber("/affordances", Affordances)
        self.affordancesCache = message_filters.Cache(sub, 10)
        rospy.loginfo("Gatherer initiated")        
        rospy.sleep(1);
        
    def gather(self):
        # Collect messages away from movement
        now = rospy.Time.now()
        
        while (self.affordancesCache.getLastestTime() != None and
               self.affordancesCache.getLastestTime() < now and
               (not rospy.is_shutdown())):
            rospy.sleep(.1)
        while (self.markersCache.getLastestTime() != None and 
               self.markersCache.getLastestTime() < now and
               (not rospy.is_shutdown())):
            rospy.sleep(.1)
               
        affs = self.affordancesCache.getElemBeforeTime(now)
        markers = self.markersCache.getElemBeforeTime(now)
        # Don't trust if more than one marker
        if len(markers.markers) > 1:
            return ([], affs.affordances)
        else:
            return (markers.markers, affs.affordances)
    
if __name__ == "__main__":
    rospy.init_node('infoGatherer')
    
    print InfoGatherer().gather()
    
    
        
