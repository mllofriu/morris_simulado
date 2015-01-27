#!/usr/bin/env python

'''
Created on May 22, 2013

@author: mllofriu
'''
import rospy

import socket
from morris_simulation.nsl import InfoGatherer
from morris_simulation.protobuf import connector_pb2 as proto

from robot_pose_fslam.srv import ResetPositionRequest, ResetPosition
from geometry_msgs.msg import Transform
from tf.transformations import *

from google.protobuf.internal import encoder
from geometry_msgs.msg import Twist
from math import pi

class NSLConnector(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        rospy.init_node('NSLConnector')
        
        # Flag that determines the validity of information gathered 
        self.validInformation = False
        self.markers = None
        self.afforances = None
        
        self.infoGatherer = InfoGatherer();
        #self.infoGatherer.gather()
        
        # Open the socket 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        s.settimeout(None)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Send every packet individually
#        host = socket.gethostname() # Get local machine name
#        print host
        port = 12345  # Reserve a port for your service.
        s.bind(("0.0.0.0", port))  # Bind to the por
        rospy.loginfo("NSLConnector initialized")
        
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        vel = Twist()
        self.cmd_vel_pub.publish(vel)
        
        rospy.loginfo("Waiting for service resetLocation")
        rospy.wait_for_service('/robot_pose_fslam/reset_position')
        try:
            self.resetLocation = rospy.ServiceProxy('/robot_pose_fslam/reset_position', ResetPosition)
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
        rospy.loginfo("Service resetLocation acquired")
        
        s.listen(5)  # Now wait for client connection.
#        while True:
        self.con, addr = s.accept()  # Establish connection with client.
#        self.processConnection()
    

    def doAction(self, angle, stop):
        print "Command", angle
        vel = Twist()
        if (not stop):
            if angle == 0:
                vel.linear.x = .1
            else:
                vel.angular.z = angle
        else:
            vel.linear.x = 0
            
        self.cmd_vel_pub.publish(vel)
            
        if (not stop):
            rospy.sleep(1)
            
            vel = Twist()
            self.cmd_vel_pub.publish(vel)
        
            
        self.validInformation = False
        # Send Ok msg
        okMsg = proto.Response()
        okMsg.ok = True;
        self.sendMsg(okMsg)
        
    def startRobot(self):
        print "Start Robot"

        # Spin 4 times to make map
#         for i in range(8):
#             vel = Twist()
#             vel.linear.x = 0
#             vel.angular.z = pi / 8
#                 
#             self.cmd_vel_pub.publish(vel)
#                 
#             rospy.sleep(1.8)
#                 
#             vel = Twist()
#             self.cmd_vel_pub.publish(vel)
#         
#             rospy.sleep(8)
        
        # Send Ok msg
        okMsg = proto.Response()
        okMsg.ok = True;
        self.sendMsg(okMsg)
        
    def resetPosition(self, pos):
        print "Reseting position"

        rp = ResetPositionRequest()
        rp.pose.translation.x = pos.x 
        rp.pose.translation.y = pos.y
        rp.pose.translation.z = 0
        rot = quaternion_from_euler(0,0,pos.theta)
        rp.pose.rotation.x = rot[0]
        rp.pose.rotation.y = rot[1]
        rp.pose.rotation.z = rot[2]
        rp.pose.rotation.w = rot[3] 
        rp.header.stamp = rospy.Time.now()
        self.resetLocation(rp)
        
        # Send Ok msg
        okMsg = proto.Response()
        okMsg.ok = True;
        self.sendMsg(okMsg)

    def getInfo(self):
#         success = False
#         while not success:
#             try:
        self.markers, self.affordances, self.robotPos = self.infoGatherer.gather()
    
        resp = proto.Response()
        resp.ok = True
        for b in self.affordances:
            resp.affs.aff.append(b)
        
        for m in self.markers:
            plm = resp.landmarks.add()
            plm.id = m[0]
            plm.x = m[1]
            plm.y = m[2]  # t[1]
            plm.z = m[3]
        
        
        resp.robotPos.x = self.robotPos[0]
        resp.robotPos.y = self.robotPos[1]
        resp.robotPos.theta = self.robotPos[2]
    
        self.sendMsg(resp)
                
#                 success = True
#             except:
#                 rospy.logerr("Exception while trying to get info")

    def sendMsg(self, resp):
        #print "Sending info"  
        data = resp.SerializeToString()
        self.con.sendall(encoder._VarintBytes(len(data)) + data)
        #print "Info sent"

    def processConnection(self):
        ended = False
        while not ended or rospy.is_shutdown():
            try:
                self.con.settimeout(60)
                text = self.con.recv(4096)
                cmd = proto.Command()
                cmd.ParseFromString(text)
                
                if cmd.type == proto.Command.doAction or cmd.type == proto.Command.rotate :
                    self.doAction(cmd.angle, cmd.stop)
                elif cmd.type == proto.Command.startRobot:
                    self.startRobot()
                elif cmd.type == proto.Command.getInfo:
                    #print "Getting info"
                    self.getInfo()
                elif cmd.type == proto.Command.resetPosition:
                    #print "Getting info"
                    self.resetPosition(cmd.pos)
                    #print "Getting info done"
                
                ended = cmd.type == proto.Command.stopRobot
            except:
                ROS_ERROR("Error while trying to comply with command, trying again in a few seconds")
                rospy.sleep(1.0)
                
            
            
       

        # Send Ok msg
        # okMsg = proto.Response()
        # okMsg.ok = True;
        # self.con.send(okMsg.SerializeToString())
    
        self.con.close()

    def __del__(self):
        self.con.close()
        
if __name__ == "__main__":
    nslC = NSLConnector()
    nslC.processConnection()
    
    
