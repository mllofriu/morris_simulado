#!/usr/bin/env python
import roslib; roslib.load_manifest('morris_simulation')
from sensor_msgs.msg import Image
import rospy

from cv2 import *
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from symbol import parameters

bridge = CvBridge()    

NO_WALL_THRS = 25

def callbackBottom(data):
    try:
        img = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    except CvBridgeError, e:
        print "Macana:", e
        
    img = resize(img,(0,0),fx=4, fy=4)

            
    grey = cvtColor(img, COLOR_BGR2GRAY)
    retval, thrs = threshold(grey, 100, 255, THRESH_BINARY)
    
    xdim,ydim = thrs.shape
    lowerhalf = thrs[xdim/2:xdim, 0:ydim]
    
    xdim, ydim = lowerhalf.shape
    subblocks = [lowerhalf[0:xdim, 0:ydim/3],
                 lowerhalf[0:xdim, (ydim/3):(ydim/3*2)],
                 lowerhalf[0:xdim, (ydim/3*2):ydim]]  
    
    affs = affordances(subblocks)
    
    print affs
    
    imshow("Original Bottom", lowerhalf)
    
def affordances(subblocks):
    sums = []
    for sublock in subblocks:
        numelements = sublock.shape[0] * sublock.shape[1]
        sums += [sublock.sum() / numelements]
    
    print sums
    return [sums[0] < NO_WALL_THRS,
            sums[1] < NO_WALL_THRS,
            sums[2] < NO_WALL_THRS]

if __name__ == '__main__':
    rospy.init_node('imshow')
    namedWindow("Original Bottom")
    rospy.Subscriber("/camera/image_raw", Image, callbackBottom)
    
    while not rospy.is_shutdown():
#            _,img = self.c.read()
#            self.detectFeatures(img)
#            rospy.sleep(self.period)
        waitKey(5)
