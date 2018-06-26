# !/bin/bash

for COLORPATH in SAT SAT_iter sim_annealing
do
	[ -e colorarrays/$COLORPATH/*.npy ] && git rm colorarrays/$COLORPATH/*.npy
done
