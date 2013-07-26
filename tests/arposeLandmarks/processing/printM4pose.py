#!/usr/bin/env python  
import roslib
roslib.load_manifest('morris_simulation')
import rospy

import tf
from visualization_msgs.msg import Marker

listener = None 

def broadcast_transform(msg):
    br = tf.TransformBroadcaster()
    
    now = rospy.Time.now()
    listener.waitForTransform("/base_footprint","/M4" , now, rospy.Duration(10.0))
    (transf,rot) = listener.lookupTransform("/base_footprint", "/M4", now)
#     br.sendTransform(transf, rot,
#                      rospy.Time.now(),
#                      "/base_footprint", 
#                      "/M4_base",
#                      )
    print transf

if __name__ == '__main__':
    rospy.init_node('landmark_abs_broadcast')
    listener = tf.TransformListener()
    rospy.Subscriber('/visualization_marker',
                     Marker,
                     broadcast_transform)
    rospy.spin()