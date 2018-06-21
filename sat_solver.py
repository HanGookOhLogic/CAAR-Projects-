import math
import pycosat
import pairs_helper

# We set up a correspondence between pixel and color pairs and positive integers 
# representing boolean variables in the CNF formula used in the SAT solver

# Converts a pixel and color pair to a corresponding unique positive integer representing a boolean variable in a CNF formula
def pixel_color_to_int(p, k, N, K):
    return (N*p[0] + p[1])*K + k + 1

# Converts an integer corresponding to a boolean variable to a unique pixel and color pair
def int_to_pixel_color(sat_var, N, K):
    square = (sat_var - 1) / K
    i = square / N
    j = square % N
    k = (sat_var - 1) % K
    return (i, j), k
    
# The number of boolean variables in the CNF formula for a coloring problem
def number_of_variables(N, K):
    return N*N*K                # There is a boolean variable for each pixel and color pair

# Sets a pixel to a certain color by appending unary clauses to the cnf formula
def set_pixel_color(cnf, i, j, color, N, K):
    for k in range(K):
        scale = -1
        if k == color:
            scale = 1
        cnf.append([scale*pixel_color_to_int((i, j), k, N, K)])
    return
    
# Given a list of pairs of adjacent pixels, this function converts the coloring problem to an equivalent CNF formula
# In this CNF formula, there is a variable for each pixel and color pair, and this set variable is set to true if we
# color that pixel with that color in a satisfying coloring
def pairs_to_SAT(pairs, S, N, K):
    cnf = []
    
    # We restrict three colors using an embedded equilateral triangle to cut out some redundant SAT solutions
    pixels_per_unit = N/float(S)
    
    # Constrain first pixel to first color to save time
    i0 = 0
    j0 = 0
    set_pixel_color(cnf, i0, j0, 0, N, K)
    
    # Constrain pixel that is a distance of 1 horizontally from (0, 0) to be second color
    i1 = 0
    j1 = int(math.floor(pixels_per_unit))
    set_pixel_color(cnf, i1, j1, 1, N, K)
    
    # Constrain third pixel equidistant from first and second with length 1
    i2 = int(math.floor(pixels_per_unit*(math.sqrt(3)/2)))
    j2 = int(math.floor(pixels_per_unit/2))
    set_pixel_color(cnf, i2, j2, 2, N, K)
    
    # For each pixel and color pair, add a clause ensuring that at least one pixel color pair set to true
    for i in range(N):
        for j in range(N):
            clause = []
            for k in range(K):
                clause.append(pixel_color_to_int((i, j), k, N, K))
            cnf.append(clause)
            
            for k1 in range(K):
                for k2 in range(k1):
                    cnf.append([-1*pixel_color_to_int((i, j), k1, N, K), -1*pixel_color_to_int((i, j), k2, N, K)])
    
    # For each pair of adjacent pixels, ensure that both are not the same color
    for pair in pairs:
        for k in range(K):
            cnf.append([-1*pixel_color_to_int(pair[0], k, N, K), -1*pixel_color_to_int(pair[1], k, N, K)])
    
    return cnf
    
# Given a satisfying assignment for the formula returned by pairs_to_SAT, this function converts it to a coloring
def solution_to_coloring(solution, N, K):
    coloring = [[0 for j in range(N)] for i in range(N)]
    num_var = number_of_variables(N, K)
    for sat_var in range(num_var):
        if solution[sat_var] > 0:
            pixel, k = int_to_pixel_color(sat_var + 1, N, K)
            coloring[pixel[0]][pixel[1]] = k
    return coloring

# Given parameters S (side length of square), N (number of pixels on side of square), K (number of colors)
# and wrapping (true if we want pixels to be adjacent accross border of square), this function uses a SAT
# solver and returns a satisfying coloring or "UNSAT" if the problem is not satisfiable
def SAT_solve(S, N, K, wrapping, itersolve=False):
    pairs = pairs_helper.list_of_pixel_pairs(S, N, wrapping, pairs_helper.Format.LIST)
    cnf = pairs_to_SAT(pairs, S, N, K)
    solution = []
    if itersolve:
        solution = pycosat.itersolve(cnf)
    else:
        solution = pycosat.solve(cnf)
    if solution == "UNSAT":
        return solution
    
    if itersolve:
        return [solution_to_coloring(sol, N, K) for sol in solution]
    else:
        return solution_to_coloring(solution, N, K)

# Like SAT_Solve but instead of returning one solution, it returns a list of all solutions
def SAT_itersolve(S, N, K, wrapping):
    return SAT_solve(S, N, K, wrapping, True)