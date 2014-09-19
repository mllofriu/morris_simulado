#!/usr/bin/env python  
'''
Created on May 22, 2013

@author: mllofriu
'''


import roslib; roslib.load_manifest('morris_simulation')
import rospy


#from affordances import Affordances
#from morris_simulation.perception import AffordanceCalc
#from MarkerCalc import MarkerCalc
from visualization_msgs.msg import  Marker
#from morris_simulation.msg import Lines
#from moveJoint import JointMover
from naoqi import ALProxy
import message_filters
from sensor_msgs.msg import Range

class InfoGatherer(object):
    '''
    classdocs
    '''
    close_thrs = .5

    def __init__(self):
        # Listen to visualization_markers for markers
        sub = message_filters.Subscriber("/visualization_marker", Marker)
        self.markersCache = message_filters.Cache(sub, 20)
        sub = message_filters.Subscriber("/nao/sonar_left",Range )
        self.sonarLeftCache = message_filters.Cache(sub, 5)
        sub = message_filters.Subscriber("/nao/sonar_right", Range)
        self.sonarRightCache = message_filters.Cache(sub, 5)

	#rospy.sleep(5.)        
        
        # Fix pitch
#        self.mover.move("HeadPitch", [.7], .5)
        rospy.loginfo( "Gatherer initiated")
        
        
    def gather(self):
        
        markers = []
	sonarLeft = []
	sonarRight = []
        # Collect messages away from movement
	now = rospy.Time.now()
        markers += self.markersCache.query(now - rospy.Duration(1), now)
	sonarLeft += self.sonarLeftCache.query(now - rospy.Duration(1), now)
	sonarRight += self.sonarRightCache.query(now - rospy.Duration(1), now)

	#print sonarRight
       	# print "Markers", markers
        marks = self.avgMarkers(markers)

	aff = self.affordances(sonarLeft, sonarRight)
        
        return (marks, aff)

    def affordances(self, sonarLeft, sonarRight):
	# If any value less than threshold
	somethingLeft = any(map(lambda msg : msg.range <= self.close_thrs, sonarLeft))
	somethingRight = any(map(lambda msg : msg.range <= self.close_thrs, sonarRight))
	# If both have something, there is something front
	somethingFront = somethingLeft and somethingRight
	return [not somethingLeft, not somethingFront, not somethingRight]
    
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
            averagedMarkers += [(k,x,y,z)]
        
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
    
    
        
