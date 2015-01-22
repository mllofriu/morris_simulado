#!/usr/bin/env python
import roslib; roslib.load_manifest('morris_simulation')
from sensor_msgs.msg import Image
import rospy

from cv2 import *
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from morris_simulation.msg import Affordances 


bridge = CvBridge()    

# Calculates affordances based on visual input
# Depends on the head being at pitch -5 degrees and yaw 0
class VisualAffCalculator(object):

    NO_WALL_THRS = 70
    debug = False
    
    def __init__(self):
        if self.debug:
            namedWindow("Original Bottom")
        rospy.init_node('visual_affordances')
        if not self.debug:
            rospy.Subscriber("image", Image, self.processImage)
        else:
            rospy.Subscriber("/nao_cam/bottom/image_raw", Image, self.processImage)
        
        self.pub = rospy.Publisher("affordances", Affordances, queue_size=1)
        if not self.debug:
            rospy.spin()
        else :
            while not rospy.is_shutdown():
                waitKey(5)
            
    def processImage(self, data):
        try:
            img = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
        except CvBridgeError, e:
            print "Macana:", e
            
        img = resize(img,(0,0),fx=4, fy=4)
    
                
        grey = cvtColor(img, COLOR_BGR2GRAY)
        
        xdim,ydim = grey.shape
        lowerhalf = grey[(3*xdim/4):xdim, 0:ydim]
        
        xdim, ydim = lowerhalf.shape
        subblocks = [lowerhalf[0:xdim, 0:ydim/3],
                     lowerhalf[0:xdim, (ydim/3):(ydim/3*2)],
                     lowerhalf[0:xdim, (ydim/3*2):ydim]]  
        
        affs = self.affordances(subblocks)
        msg = Affordances()
        msg.header.stamp = rospy.Time.now()
        msg.affordances = affs
        self.pub.publish(msg)    

        if self.debug:
            print affs
            imshow("Original Bottom", lowerhalf)

    def affordances(self, subblocks):
        sums = []
        for sublock in subblocks:
            numelements = sublock.shape[0] * sublock.shape[1]
            sums += [sublock.sum() / numelements]
        
        if self.debug:
            print sums
        
        somethingleft = sums[0] >= self.NO_WALL_THRS
        somethingright = sums[2] >= self.NO_WALL_THRS 
        somethingfront = sums[1] >= self.NO_WALL_THRS or somethingleft or somethingright
        return [not somethingright,
                not somethingfront,
                not somethingleft]

if __name__ == '__main__':
    VisualAffCalculator()
    #namedWindow("Original Bottom")
   