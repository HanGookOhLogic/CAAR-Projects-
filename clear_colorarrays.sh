# !/bin/bash

for COLORPATH in SAT SAT_iter sim_annealing
do
	[ -e colorarrays/$COLORPATH/*.npy ] && rm colorarrays/$COLORPATH/*.npy
done
