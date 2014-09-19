#!/usr/bin/python
import roslib
roslib.load_manifest('morris_simulation')

import rospy
from visualization_msgs.msg import  Marker
from naoqi import ALProxy
import message_filters

import math

def moveJoint(joint, motionProxy, angleChange, vel):
	names            = joint
	changes          = angleChange
	fractionMaxSpeed = vel
	motionProxy.changeAngles(names, changes, fractionMaxSpeed)


if __name__ == '__main__':
	rospy.loginfo("Starting marker follower...")
	rospy.init_node('headMarkerFollower')
	sub = message_filters.Subscriber("/visualization_marker", Marker)
	markersCache = message_filters.Cache(sub, 50)

	try:
		motionProxy = ALProxy("ALMotion", '127.0.0.1', 9559)
    	except Exception, e:
		print "Could not create proxy"

    	# Init stiffness
	motionProxy.setStiffnesses("Head", 1.0)
    	motionProxy.setSmartStiffnessEnabled(True) 

   	r = rospy.Rate(10) 
	goingLeft = True
	while not rospy.is_shutdown():
		# Obtengo los del ultimo seg
		now = rospy.Time.now()
		markers = markersCache.query(now - rospy.Duration(1),now)
		# Los cuento
		numMarkers = len(markers)
		# Si hay alguno
		if (numMarkers >= 1):
			print "Vi hace un segundo por lo menos"
			# Posicion del ultimo -> pos
			lastM = markers[numMarkers-1]
			x = lastM.pose.position.x
			y = lastM.pose.position.y
			print x, y
			px =  x / .40
			py = y / .40
			anglex = -math.copysign(.1 * abs(px), px)
			angley = math.copysign(.1 * abs(py), py)
			velx = abs(px) * 0.4
			vely = abs(py) * 0.4
			moveJoint ("HeadYaw",motionProxy,anglex, velx)

			pitch = motionProxy.getAngles("HeadPitch",True)[0]
			# if im not trying to go up when already looking up
			if not ((pitch > .3 and angley > 0) or (pitch < -.3 and angley < 0)):
				moveJoint ("HeadPitch",motionProxy,angley, vely)
				# control de yaw = P(pos.x)
		else :
			print "No veo!"
			yaw = motionProxy.getAngles("HeadYaw",True)[0]
			print yaw
			print goingLeft
			if (goingLeft):
				if (yaw < 1):
					anglex = .1
				else:
					anglex = -.1
					goingLeft = False
			else:
				if (yaw > -1):
                                        anglex = -.1
                                else:
                                        anglex = .1
                                        goingLeft = True
			print anglex
			moveJoint ("HeadYaw",motionProxy,anglex,.2)
			# Si no hay ninguno
				# Scan
		r.sleep()
