import simulated_annealing
import printColourGrid
import numpy

# CONSTANTS
S = 4 # Side length of nxn square
N = 20 # Number of pixels on one side of square
K = 7 # Number of colors
WRAPPING = False # Whether or not we wrap distances across edges of square when finding pairs of pixels unit distaqnce from each other
INIT_TEMP = 10 # Initial temperature for the simulated annealing algorithm
COOLING_RATE = 0.15 # Cooling rate for the simulated annealing algorithm. Each iteration, T is multiplied by (1-cooling_rate);



# use simulated annealing to find an optimal coloring given the parameters
coloring, cost = simulated_annealing.simulated_annealing(S, N, K, WRAPPING, INIT_TEMP, COOLING_RATE)

# create image file name
wrappingString = 'False'
if WRAPPING:
    wrappingString = 'True'
name = 's' + str(S) + '_n' + str(N) + '_k' + str(K) + '_wrapping' + wrappingString + '_temp' + str(INIT_TEMP) + '_cr' + str(int(COOLING_RATE*100)) + '_cost' + str(cost)

numpy.save(name, coloring)



# save coloring as an image
#printColourGrid.create_coloring(coloring, N, K, name)