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
import tf 

class InfoGatherer(object):
    '''
    classdocs
    '''

    close_thrs = 3.
    
    def __init__(self):
        self.tf_listener = tf.TransformListener()
        sub = message_filters.Subscriber("/ar_pose/ar_pose_marker", ARMarkers)
        self.markersCache = message_filters.Cache(sub, 10)
        sub = message_filters.Subscriber("/affordances", Affordances)
        self.affordancesCache = message_filters.Cache(sub, 10)
        
        rospy.loginfo("Gatherer initiated")        
        
    def gather(self):
        # Collect messages away from movement
        now = rospy.Time.now()
        waited = False
        
        while (self.affordancesCache.getLastestTime() != None and
               self.affordancesCache.getLastestTime() < now and
               (not rospy.is_shutdown())):
            rospy.sleep(1)
            waited = True
        
        markers = []

        for id in range(4):
            try:
                if waited:
                    time = rospy.Duration(0.01)
                else:
                    time = rospy.Duration(1)
                    waited = True
                self.tf_listener.waitForTransform("robot", "slam/M" + str(id + 1), now, time)
                (t, rot) = self.tf_listener.lookupTransform("robot", "slam/M" + str(id + 1), rospy.Time(0))
                # Only add landmark if closer than threshold
                print "Marca (id, x, y)", (id, t[0], t[1]) 
                if t[0] < self.close_thrs:
                    markers += [(id,t[0],t[1],0)]
            except:
                 rospy.loginfo("No transform for landmark slam/M%s",  str(id + 1));
        
               
        affs = self.affordancesCache.getElemBeforeTime(now)
        # Don't trust if more than one marker
        
        return (markers, affs.affordances)
    
if __name__ == "__main__":
    rospy.init_node('infoGatherer')
    
    g = InfoGatherer()
    rospy.sleep(1)
    print g.gather()
    
    
        
