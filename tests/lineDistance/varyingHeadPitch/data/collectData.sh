#!/usr/bin/env sh

for i in `seq -10 5 20`; do
	echo "Presione enter para grabar " $i "mm"
	read line
	# record everything just in case
	rosbag record -l 20 /line_vis_markers -O ${i}degrees.bag
done
