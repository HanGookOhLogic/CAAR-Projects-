To run the program, run 'coloring.py'.
For help on different coloring algorithm options, run 'python coloring.py -h'.

TO RUN AN INTERACTIVE GPU SESSION IN GRACE:
qsub interGPU.pbs

TO RUN A JOB ON THE GPU WITHOUT NEEDING TO STAY CONNECTED TO GRACE:
qsub -v ARGS="[arguments]" queueGPU.pbs
e.g. qsub -v ARGS="-n50 -k7 -s4 --sim" queueGPU.pbs
Type "qstat" to check if job is finished running. When job finishes, stdout will be in file "Job_output.txt"
