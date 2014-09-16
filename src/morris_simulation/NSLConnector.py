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
        
        # Open the socket 
        s = socket.socket()         # Create a socket object
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
        self.pilot = Pilot()
        self.infoGatherer = InfoGatherer();
        # Send Ok msg
        okMsg = rp.Response()
        okMsg.ok = True;
        serial = okMsg.SerializeToString()
        print "Largo", len(serial)
        print "Msg", serial
        self.con.sendall(serial)
        print "ok sent"
#                con.flush()

    def getAffordances(self):
        print "Affordances"
        if not self.validInformation:
            self.affordances, self.markers = self.infoGatherer.gather()
            self.validInformation = True
        print "Affordances obtained", self.affordances
        self.sendAffordances(self.affordances,self.con)
        print "affordances sent"
                
    def isThereFood(self):
        print "Is there food?"
        
    def getMarcas(self):
        print "GetMarcas"
        if not self.validInformation:
            self.affordances, self.markers = self.infoGatherer.gather()
            self.validInformation = True
        
    def processConnection(self):
        cmd = rp.Command()
        text = self.con.recv(4096)
        cmd.ParseFromString(text)
        
        while cmd.command != rp.Command.close:
            if cmd.command == rp.Command.doAction or cmd.command == rp.Command.rotate :
                self.doAction(cmd.angle)
            elif cmd.command == rp.Command.startRobot:
                self.startRobot()
            elif cmd.command == rp.Command.getAffordances:
                self.getAffordances()
            elif cmd.command == rp.Command.isFood:
                self.isThereFood()
            elif cmd.command == rp.Command.getMarcas:
                self.getMarcas()
            
            
            
            text = self.con.recv(4096)
            cmd.ParseFromString(text)
        
        SitDown()
        # Send Ok msg
        okMsg = rp.Response()
        okMsg.ok = True;
        self.con.send(okMsg.SerializeToString())
    
    def sendAffordances(self, affordances, con):    
        affMsg = rp.Affordances()
        for af in affordances:
            affMsg.affordance.append(af)
        
        con.sendall(affMsg.SerializeToString())
        
    def sendMarkers(self, markers, con):
        affMsg = rp.Marcas()
    
    def __del__(self):
        self.con.close()
        
if __name__ == "__main__":
    nslC = NSLConnector()
    nslC.processConnection()
    nslC.getAffordances()
    
    