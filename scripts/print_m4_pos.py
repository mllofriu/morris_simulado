#!/usr/bin/env python  
import roslib
roslib.load_manifest('morris_simulation')
import rospy
import sys
import tf
from visualization_msgs.msg import Marker
import math

listener = None 
samples = 0

def broadcast_transform(msg):
    global samples 
    
    br = tf.TransformBroadcaster()
    
    now = rospy.Time.now()
    listener.waitForTransform("/base_footprint","/M4" , now, rospy.Duration(10.0))
    (transf,rot) = listener.lookupTransform("/base_footprint", "/M4", now)
#     br.sendTransform(transf, rot,
#                      rospy.Time.now(),
#                      "/base_footprint", 
#                      "/M4_base",
#                      )
    distance = math.sqrt( transf[0]**2 + transf[1]**2)
    print sys.argv[1],distance
    samples += 1
    if samples >= int(sys.argv[2]):
        rospy.signal_shutdown(0)
        
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage:", sys.argv[0], "distance", "samples"
        exit(1)
    
    rospy.init_node('print_m4_pos')
    listener = tf.TransformListener()
    rospy.Subscriber('/visualization_marker',
                     Marker,
                     broadcast_transform)
    while not rospy.is_shutdown():
        rospy.spin()