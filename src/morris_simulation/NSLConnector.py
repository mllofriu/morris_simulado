#!/usr/bin/env python

'''
Created on May 22, 2013

@author: mllofriu
'''
import roslib; roslib.load_manifest('morris_simulation')
import rospy

import socket
from morris_simulation.nsl import InfoGatherer
from morris_simulation.protobuf import connector_pb2 as proto
import tf 

from naoqi import ALProxy

from google.protobuf.internal import encoder

class NSLConnector(object):
    '''
    classdocs
    '''

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
        
        s.listen(5)  # Now wait for client connection.
#        while True:
        self.con, addr = s.accept()  # Establish connection with client.
#        self.processConnection()
        try:
            self.motionProxy = ALProxy("ALMotion", 'elvira', 9559)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e
            exit(1)
            
        try:
            self.postureProxy = ALProxy("ALRobotPosture", 'elvira', 9559)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
            exit(1)
    

    def doAction(self, angle):
        print "Command", angle
        if angle == 0:
            x = .05
            y = 0
            t = 0
            f = .5
        else:
            x = 0
            y = 0
            t = angle 
            f = .5 
#         self.motionProxy.setWalkTargetVelocity(x, y, t, f)  
        if angle == 0:
            rospy.sleep(2) 
        else :
            rospy.sleep(2)
        self.motionProxy.moveTo(x, y, t, [["MaxStepFrequency", .8], ["MaxStepX", 0.02]])
        self.motionProxy.setWalkTargetVelocity(0, 0, 0, 0)  
        self.validInformation = False
        # Send Ok msg
        okMsg = proto.Response()
        okMsg.ok = True;
        self.sendMsg(okMsg)
        
    def startRobot(self):
        print "Start Robot"

        # Send NAO to Pose Init
        self.motionProxy.setSmartStiffnessEnabled(True)
        self.postureProxy.goToPosture("StandInit", 0.5) 
        
        names = "HeadPitch"
        angleLists = [.1, -.2]
        timeLists = [.5, 1]
        isAbsolute = True
        self.motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
        
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
        print(self.affordances)
        for b in self.affordances:
            resp.affs.aff.append(b)
    
        for lm in self.markers:
            try:
                self.tf_listener.waitForTransform("/base_footprint", "/M" + str(lm[0] + 1), rospy.Time(), rospy.Duration(3))
                (t, rot) = self.tf_listener.lookupTransform("/base_footprint", "/M" + str(lm[0] + 1), rospy.Time(0))
            
                plm = resp.landmarks.add()
                # lm = (id, x, y, z) - x, y and z are not used since the transform is published
                plm.id = lm[0]
                # self.tf_listener.waitForTransform("/base_footprint","/M"  + str(plm.id + 1), now, rospy.Duration(.3))
		# Transform coordinates from robot to model: x is the same, z is y and y = 0 (height)
                plm.x = t[0]
                plm.y = 0  # t[1]
                plm.z = -t[1]  # t[2]
		print "Marca", (t[0], -t[1]) 
                # resp.landmarks.append(lm)
            except:
                rospy.loginfo("Exception while trying to lookup transform") 

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
        
        while cmd.type != proto.Command.stopRobot:
            if cmd.type == proto.Command.doAction or cmd.type == proto.Command.rotate :
                self.doAction(cmd.angle)
            elif cmd.type == proto.Command.startRobot:
                self.startRobot()
            elif cmd.type == proto.Command.getInfo:
                print "Getting info"
                self.getInfo()
                print "Getting info done"
            
            text = self.con.recv(4096)
            cmd = proto.Command()
            cmd.ParseFromString(text)
       
        self.postureProxy.goToPosture("Crouch", 0.5)    
        self.motionProxy.rest()

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
    
    
