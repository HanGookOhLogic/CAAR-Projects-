import sat_solver
import printColourGrid
import numpy

# CONSTANTS
S = 4 # Side length of nxn square
N = 19 # Number of pixels on one side of square
K = 7 # Number of colors
WRAPPING = False # Whether or not we wrap distances across edges of square when finding pairs of pixels unit distaqnce from each other
ITER = False # Whether to find search for every solution. If ITER = False, the program terminates as soon as the first solution is found


wrappingString = 'False'
if WRAPPING:
    wrappingString = 'True'

folderString = 'SAT/'
if ITER:
    folderString = 'SAT_iter/'
   
name = folderString + 's' + (str(S)).replace('.',',') + '_n' + str(N) + '_k' + str(K) + '_wrapping' + wrappingString

if ITER:
    colorings = sat_solver.SAT_itersolve(S, N, K, WRAPPING)
    if not colorings:
        print "This coloring problem is unsatisfiable."
    else:
        name += '_iter'
        i = 0
        for coloring in colorings:
            printColourGrid.create_coloring(coloring, N, K, name + str(i))
            i += 1
else:
    coloring = sat_solver.SAT_solve(S, N, K, WRAPPING)
    if coloring == "UNSAT":
        print "This coloring problem is unsatisfiable."
    else:
        printColourGrid.create_coloring(coloring, N, K, name)


"""
coloring = sat_solver.SAT_itersolve(S, N, K, WRAPPING)
if not coloring:
    print "This coloring problem is unsatisfiable."
else:
    wrappingString = 'False'
    if WRAPPING:
        wrappingString = 'True'
    name = 'SAT_iter/s' + (str(S)).replace('.',',') + '_n' + str(N) + '_k' + str(K) + '_wrapping' + wrappingString + '_iter'
    
    i = 0
    for col in coloring:
        printColourGrid.create_coloring(col, N, K, name + str(i))
        i += 1
"""
        
        
        
        
"""
# create image file name
wrappingString = 'False'
if WRAPPING:
    wrappingString = 'True'
name = 's' + str(S) + '_n' + str(N) + '_k' + str(K) + '_wrapping' + wrappingString + '_temp' + str(INIT_TEMP) + '_cr' + str(int(COOLING_RATE*100)) + '_cost' + str(cost)

numpy.save(name, coloring)



# save coloring as an image
#printColourGrid.create_coloring(coloring, N, K, name)
"""