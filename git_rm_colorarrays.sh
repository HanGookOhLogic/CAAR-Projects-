# !/bin/bash

for COLORPATH in SAT SAT_iter sim_annealing
do
	for FILENAME in colorarrays/$COLORPATH/*.npy
	do
		[ -e "$FILENAME" ] && git rm "$FILENAME"
	done
done
