#!/usr/bin/env python

import rospy


from robot_pose_fslam.srv import ResetPositionRequest, ResetPosition
from geometry_msgs.msg import Transform
from tf.transformations import *
from math import pi

if __name__ == "__main__":
    rospy.init_node('reset_pose_test')
    rospy.loginfo("Waiting for service resetLocation")
    rospy.wait_for_service('/robot_pose_fslam/reset_position')
    try:
        resetLocation = rospy.ServiceProxy('/robot_pose_fslam/reset_position', ResetPosition)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
    rospy.loginfo("Service resetLocation acquired")
    
    rp = ResetPositionRequest()
    rp.pose.translation.x = .0
    rp.pose.translation.y = .0
    rp.pose.translation.z = 0
    rot = quaternion_from_euler(0,0,pi/2)
    rp.pose.rotation.x = rot[0]
    rp.pose.rotation.y = rot[1]
    rp.pose.rotation.z = rot[2]
    rp.pose.rotation.w = rot[3] 
    rp.header.stamp = rospy.Time.now()
    resetLocation(rp)

    
