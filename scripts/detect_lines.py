#!/usr/bin/env python

import roslib; roslib.load_manifest('morris_simulation')  # @UnresolvedImport
import rospy  # @UnresolvedImport

from morris_simulation.perception import LineDetector

if __name__ == "__main__":
    detector = LineDetector()
    
    while not rospy.is_shutdown():
        rospy.spin()