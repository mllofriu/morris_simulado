#!/usr/bin/env sh

for i in `seq 100 100 1000`; do
	echo "Presione enter para grabar " $i "mm"
	read line
	# record everything just in case
	rosbag record -l 20 /line_vis_markers -O ${i}mm.bag
done
