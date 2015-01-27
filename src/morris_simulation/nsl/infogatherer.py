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
from tf.transformations import euler_from_quaternion

class InfoGatherer(object):
    '''
    classdocs
    '''

    close_thrs = .5
    initial_sleep = 0
    max_wait = 2
    
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

        rospy.sleep(self.initial_sleep)
        
        while (self.affordancesCache.getLastestTime() != None and
               self.affordancesCache.getLastestTime() < now and
               (not rospy.is_shutdown())):
            rospy.sleep(now - rospy.Time.now() + rospy.Duration(self.max_wait))
        affs = self.affordancesCache.getElemBeforeTime(now)
        
        markers = []
        for id in range(4):
            try:
                self.tf_listener.waitForTransform("robot", "slam/M" + str(id + 1), now, 
                                                  now - rospy.Time.now() + rospy.Duration(self.max_wait))
                (t, rot) = self.tf_listener.lookupTransform("robot", "slam/M" + str(id + 1), now)
                # Only add landmark if closer than threshold
                print "Marca (id, x, y)", (id, t[0], t[1]) 
                if t[0]**2 + t[1] ** 2 < self.close_thrs ** 2:
                    markers += [(id,t[0],t[1],0)]
            except:
                 rospy.logdebug("No transform for landmark slam/M%s",  str(id + 1));
        
        robotPos = None
        try:
            self.tf_listener.waitForTransform("map", "robot", now, 
                                              rospy.Duration(self.max_wait))
            (t, rot) = self.tf_listener.lookupTransform("map", "robot", now)
            theta = euler_from_quaternion(rot)[2]
            # Only add landmark if closer than threshold
            print "Robot (x, y, theta)", (t[0], t[1], theta) 
            robotPos = (t[0], t[1], theta)
        except:
            rospy.logerr("No transform to robot!!!")
        
        # Don't trust if more than one marker
        
        return (markers, affs.affordances, robotPos)
    
if __name__ == "__main__":
    rospy.init_node('infoGatherer')
    
    g = InfoGatherer()
    rospy.sleep(1)
    print g.gather()
    
    
        
