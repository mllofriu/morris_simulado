#!/usr/bin/env python

import rosbag
import os
import sys
import math
import re 

if len(sys.argv) < 2:
	print "Usage:", sys.argv[0], "dirWithDataBags"

directory = sys.argv[1]

filenames = os.listdir(directory)
for f in filenames:
	#print f
	if f.endswith(".bag"):
		bag = rosbag.Bag(directory+f)
	
		m = re.search("(\d+)mm", f)
		knownDist = int(m.group(1))/1000.

		# list of meassured x of lines - x is the min x coordinate of all lines in a msg
		xMeassures = []
		for topic, msg, t in bag.read_messages():
			# Find minimum x coord among all detected lines in the message
			minX = 1000000000
			found = False
			if len(msg.markers) > 0:
				lineEnds = msg.markers[0].points
				for le in lineEnds:
					if le.x < minX:
						minX = le.x
						found = True
				xMeassures += [minX]
			if found:
				print knownDist, minX
		
		bag.close()
