#!/usr/bin/env python

import rosbag
import os
import sys
import math

if len(sys.argv) < 2:
	print "Usage:", sys.argv[0], "dirWithDataBags"

directory = sys.argv[1]

filenames = os.listdir(directory)
for f in filenames:
	#print f
	bag = rosbag.Bag(directory+f)
	
	# Calc average
	dists = []
	for topic, msg, t in bag.read_messages():
		x = msg.pose.position.x
		y = msg.pose.position.y
		d = math.sqrt(x**2 + y**2)
		dists += [d]

	if len(dists) == 0:
		print "File", directory+f,"empty"
		exit(1)

	average = sum(dists)/len(dists)
	
	# Calc variance
	stddev = 0
	for d in dists:
		stddev += (d - average) ** 2
	var = math.sqrt(stddev/len(dists))
	
	print directory+f, average, var

	bag.close()
