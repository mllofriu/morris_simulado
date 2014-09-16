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

from naoqi import ALProxy

from google.protobuf.internal import encoder

class NSLConnector(object):
    '''
    classdocs
    '''

    pilot = 0
    
    def __init__(self):
        rospy.init_node('NSLConnector')
        
        # Flag that determines the validity of information gathered 
        self.validInformation = False
        self.markers = None
        self.afforances = None
        
	self.infoGatherer = InfoGatherer();
        
        # Open the socket 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # Send every packet individually
#        host = socket.gethostname() # Get local machine name
#        print host
        port = 12345                # Reserve a port for your service.
        s.bind(("0.0.0.0", port))        # Bind to the por
        rospy.loginfo( "NSLConnector initialized")
        
        s.listen(5)                 # Now wait for client connection.
#        while True:
        self.con, addr = s.accept()     # Establish connection with client.
#        self.processConnection()
	try:
	        self.motionProxy = ALProxy("ALMotion", '127.0.0.1', 9559)
	except Exception, e:
		print "Could not create proxy to ALMotion"
		print "Error was: ", e
	try:
	        self.postureProxy = ALProxy("ALRobotPosture", '127.0.0.1', 9559)
    	except Exception, e:
        	print "Could not create proxy to ALRobotPosture"
        	print "Error was: ", e
	

    def doAction(self, angle):
        print "Command",angle
        if angle == 0:
            self.pilot.forwardMeters(.4)
        else:
            self.pilot.rotateRad(angle*pi/180)
        rospy.sleep(3)
        self.validInformation = False
        
        # Send Ok msg
        okMsg = rp.Response()
        okMsg.ok = True;
        self.con.sendall(okMsg.SerializeToString())
        
    def startRobot(self):
        print "Start Robot"

	# Send NAO to Pose Init
	self.motionProxy.setSmartStiffnessEnabled(True)
    	self.postureProxy.goToPosture("StandInit", 0.5)	

        # Send Ok msg
        okMsg = proto.Response()
        okMsg.ok = True;
        serial = okMsg.SerializeToString()
        print "Largo", len(serial)
        print "Msg", serial
        self.con.sendall(serial)
        print "ok sent"
#                con.flush()

    def getInfo(self):
        if not self.validInformation:
            self.markers, self.affordances = self.infoGatherer.gather()
	    print self.markers, self.affordances
            self.validInformation = True
	                
	resp = proto.Response()
	resp.ok = True
	for b in self.affordances:
		resp.affs.aff.append(b)
	for lm in self.markers:
		lm = proto.Landmark()
		lm.id = lm[0]
		lm.x = lm[1]
		lm.y = lm[2]
		lm.z = lm[3]
		resp.landmarks.append(lm)
      
	print "Sending info"  
	data = resp.SerializeToString()
        self.con.sendall(encoder._VarintBytes(len(data)) + data)
	print "Info sent"
     
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
                self.getInfo()
            
            text = self.con.recv(4096)
            cmd = proto.Command()
            cmd.ParseFromString(text)
       
    	self.postureProxy.goToPosture("Crouch", 0.5)	
	self.motionProxy.rest()

        # Send Ok msg
        #okMsg = proto.Response()
        #okMsg.ok = True;
        #self.con.send(okMsg.SerializeToString())
    
        self.con.close()

    def __del__(self):
        self.con.close()
        
if __name__ == "__main__":
    nslC = NSLConnector()
    nslC.processConnection()
    
    
