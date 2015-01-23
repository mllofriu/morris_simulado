#!/usr/bin/env python

'''
Created on May 22, 2013

@author: mllofriu
'''
import rospy

import socket
from morris_simulation.nsl import InfoGatherer
from morris_simulation.protobuf import connector_pb2 as proto
import tf 

from google.protobuf.internal import encoder
from geometry_msgs.msg import Twist

class NSLConnector(object):
    '''
    classdocs
    '''
    
    close_thrs = 3.

    def __init__(self):
        rospy.init_node('NSLConnector')

        self.tf_listener = tf.TransformListener()
        
        # Flag that determines the validity of information gathered 
        self.validInformation = False
        self.markers = None
        self.afforances = None
        
        self.infoGatherer = InfoGatherer();
        
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
        
        s.listen(5)  # Now wait for client connection.
#        while True:
        self.con, addr = s.accept()  # Establish connection with client.
#        self.processConnection()
    

    def doAction(self, angle):
        print "Command", angle
        vel = Twist()
        if angle == 0:
            vel.linear.x = .1
        else:
            vel.angular.z = angle/2
        
        self.cmd_vel_pub.publish(vel)
        
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

        # Send Ok msg
        okMsg = proto.Response()
        okMsg.ok = True;
        self.sendMsg(okMsg)

    def getInfo(self):
        if not self.validInformation:
            self.markers, self.affordances = self.infoGatherer.gather()
            # self.validInformation = True

        resp = proto.Response()
        resp.ok = True
        #print(self.affordances)
        for b in self.affordances:
            resp.affs.aff.append(b)
        
        # If have seen markers, look for them
#         if (len(self.markers) > 0):
#             for lm in self.markers:
#                 try:
#                     self.tf_listener.waitForTransform("robot", "/M" + str(lm.id + 1), rospy.Time(), rospy.Duration(3))
#                     (t, rot) = self.tf_listener.lookupTransform("robot", "/M" + str(lm.id + 1), rospy.Time(0))
#                     # Only add landmark if closer than threshold
#                     print "Marca", (t[0], t[1]) 
#                     if t[0] < self.close_thrs:
#                         plm = resp.landmarks.add()
#                         plm.id = lm.id
#                         plm.x = t[0]
#                         plm.y = t[1]  # t[1]
#                         plm.z = 0
#                         
#                 except:
#                      ROS_DEBUG("No transform for landmark /M%s",  str(lm.id + 1));
#         # If not, look for slam markers
#         else :
        for id in range(4):
            try:
                self.tf_listener.waitForTransform("robot", "slam/M" + str(id + 1), rospy.Time(), rospy.Duration(3))
                (t, rot) = self.tf_listener.lookupTransform("robot", "slam/M" + str(id + 1), rospy.Time(0))
                # Only add landmark if closer than threshold
                print "Marca (id, x, y)", (id, t[0], t[1]) 
                if t[0] < self.close_thrs:
                    plm = resp.landmarks.add()
                    plm.id = id
                    plm.x = t[0]
                    plm.y = t[1]  # t[1]
                    plm.z = 0
                    
            except:
                 rospy.logdebug("No transform for landmark slam/M%s",  str(id + 1));
        
        
        self.sendMsg(resp)

    def sendMsg(self, resp):
        #print "Sending info"  
        data = resp.SerializeToString()
        self.con.sendall(encoder._VarintBytes(len(data)) + data)
        #print "Info sent"

    def processConnection(self):
        cmd = proto.Command()
        text = self.con.recv(4096)
        cmd.ParseFromString(text)
        
        while cmd.type != proto.Command.stopRobot or rospy.is_shutdown():
            if cmd.type == proto.Command.doAction or cmd.type == proto.Command.rotate :
                self.doAction(cmd.angle)
            elif cmd.type == proto.Command.startRobot:
                self.startRobot()
            elif cmd.type == proto.Command.getInfo:
                #print "Getting info"
                self.getInfo()
                #print "Getting info done"
            
            text = self.con.recv(4096)
            cmd = proto.Command()
            cmd.ParseFromString(text)
       

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
    
    
