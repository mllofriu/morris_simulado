#!/usr/bin/env python  
'''
Created on May 22, 2013

@author: mllofriu
'''


import rospy


from visualization_msgs.msg import  Marker
import message_filters
from morris_simulation.msg import Affordances
from ar_pose.msg import ARMarker

class InfoGatherer(object):
    '''
    classdocs
    '''
    close_thrs = .5

    def __init__(self):
        # Listen to visualization_markers for markers
        sub = message_filters.Subscriber("/ar_pose/visualization_marker", Marker)
        self.markersCache = message_filters.Cache(sub, 10)
        sub = message_filters.Subscriber("/affordances", Affordances)
        self.affordancesCache = message_filters.Cache(sub, 10)
        rospy.loginfo("Gatherer initiated")        
        rospy.sleep(1);
        
    def gather(self):
        # Sleep to fill caches with recent info
        # rospy.sleep(.5)
        
        affs = []
        markers = []
        # Collect messages away from movement
        now = rospy.Time.now()
        
        # rospy.wait_for_message("/ar_pose/ar_pose_marker", ARMarker)        
        while (self.affordancesCache.getLastestTime() != None and self.affordancesCache.getLastestTime() < now):
            rospy.sleep(.1)
               
        affs += [self.affordancesCache.getElemBeforeTime(now)]
        markers += self.markersCache.getInterval(now - rospy.Duration(1), now)
        
        marks = self.avgMarkers(markers)
#         markerClose = len(marks) > 0 and marks[0][1] < 2.0
        
        # All affordances in true if there is a landmark close
        affordances = [a for a in affs[0].affordances]
        
        return (marks, affordances)

#     def affordances(self, sonarLeft, sonarRight, marks):
#         # If there are landmarks, ignore affordances
#         noMarks = len(marks) == 0
#         # If any value less than threshold
#         somethingLeft = noMarks and any(map(lambda msg : msg.range <= self.close_thrs, sonarLeft))
#         somethingRight = noMarks and any(map(lambda msg : msg.range <= self.close_thrs, sonarRight))
#         # If both have something, there is something front
#         somethingFront = somethingLeft and somethingRight
#         return [not somethingLeft, not somethingFront, not somethingRight]
    
    def avgMarkers(self, visMarkers):
        markerSamples = {}
        for vm in visMarkers:
            if not vm.id in markerSamples.keys():
                markerSamples[vm.id] = []
            
            markerSamples[vm.id] += [vm.pose.position]
        
        averagedMarkers = []
        for k in markerSamples.keys():
            x = 0; y = 0; z = 0;
            for ms in markerSamples[k]:
                x += ms.x
                y += ms.y
                z += ms.z
            x /= len(markerSamples[k])
            y /= len(markerSamples[k])
            z /= len(markerSamples[k])
            averagedMarkers += [(k, x, y, z)]
        
        return averagedMarkers
    
if __name__ == "__main__":
    rospy.init_node('infoGatherer')

#    try:
#        motionProxy = ALProxy("ALMotion", "127.0.0.1", 9559)
#        motionProxy.wakeUp()
#    except Exception, e:
#        print "Could not create proxy to ALMotion"
#        print "Error was: ", e
    
    
    print InfoGatherer().gather()
    
    
        
