import simulated_annealing
import printColourGrid

# CONSTANTS
S = 4 # Side length of nxn square
N = 20 # Number of pixels on one side of square
K = 7 # Number of colors
WRAPPING = False # Whether or not we wrap distances across edges of square when finding pairs of pixels unit distaqnce from each other
INIT_TEMP = 10 # Initial temperature for the simulated annealing algorithm
COOLING_RATE = 0.1 # Cooling rate for the simulated annealing algorithm. Each iteration, T is multiplied by (1-cooling_rate);

coloring, cost = simulated_annealing.simulated_annealing(S, N, K, WRAPPING, INIT_TEMP, COOLING_RATE)
print cost