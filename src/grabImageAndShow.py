#!/usr/bin/env python
import roslib; roslib.load_manifest('morris_simulation')
from sensor_msgs.msg import Image
import rospy

from cv2 import *
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from symbol import parameters

bridge = CvBridge()    

def callbackBottom(data):
    try:
        img = bridge.imgmsg_to_cv(data, desired_encoding="passthrough")
    except CvBridgeError, e:
        print "Macana:", e
        
    img = np.asarray(img)
            
    canny = Canny(img, 100, 200)
    lines = HoughLinesP(canny, 1, cv.CV_PI/180, 50, minLineLength=10,maxLineGap=3)
    
    #if (lines != None):
    #    for l in lines[0]:
    #        #rospy.loginfo(l)
    #        line(img, (l[0], l[1]),(l[2],l[3]), cv.CV_RGB(255, 0, 0), 3, 8)
    
    imshow("Original Bottom", img)
    
    
def callbackTop(data):
    try:
        img = bridge.imgmsg_to_cv(data,desired_encoding="bgr8")
    except CvBridgeError, e:
        print "Macana:", e
        
    img = np.asarray(img)

    imshow("Original Top", img)


if __name__ == '__main__':
    rospy.init_node('imshow')
    namedWindow("Original Bottom")
    namedWindow("Original Top")
    rospy.Subscriber("/nao_cam/bottom/image_raw", Image, callbackBottom)
    rospy.Subscriber("/nao_cam/top/image_raw", Image, callbackTop)
    
    while not rospy.is_shutdown():
#            _,img = self.c.read()
#            self.detectFeatures(img)
#            rospy.sleep(self.period)
        waitKey(5)
