import math
import pycosat
import pairs_helper

# We set up a correspondence between pixel and color pairs and positive integers 
# representing boolean variables in the CNF formula used in the SAT solver

def get_bit(int, b):
    return (int >> b) & 1
    
def set_bit(int, b):
    return (int | (1 << b))
    
def scale_bit(b):
    return 2*b - 1

# Converts a pixel and color pair to a corresponding unique positive integer representing a boolean variable in a CNF formula
def pixel_bit_to_int(p, b, N, B):
    return (N*p[0] + p[1])*B + b + 1

# Converts an integer corresponding to a boolean variable to a unique pixel and color pair
def int_to_pixel_bit(sat_var, N, B):
    square = (sat_var - 1) / B
    i = square / N
    j = square % N
    b = (sat_var - 1) % B
    return (i, j), b
    
# The number of boolean variables in the CNF formula for a coloring problem
def number_of_variables(N, B):
    return N*N*B                # There is a boolean variable for each pixel and color pair

# Sets a pixel to a certain color by appending unary clauses to the cnf formula
def set_pixel_color(cnf, i, j, color, N, B):
    bit_scale = [scale_bit(get_bit(color, b)) for b in range(B)]
    for b in range(B):
        cnf.append([bit_scale[b]*pixel_bit_to_int((i, j), b, N, B)])
    return
    
# Given a list of pairs of adjacent pixels, this function converts the coloring problem to an equivalent CNF formula
# In this CNF formula, there is a variable for each pixel and color pair, and this set variable is set to true if we
# color that pixel with that color in a satisfying coloring
def pairs_to_SAT(pairs, S, N, B, K):
    cnf = []
    
    # We restrict three colors using an embedded equilateral triangle to cut out some redundant SAT solutions
    pixels_per_unit = N/float(S)
    
    # Constrain first pixel to first color to save time
    i0 = 0
    j0 = 0
    set_pixel_color(cnf, i0, j0, 0, N, B)
    
    # Constrain pixel that is a distance of 1 horizontally from (0, 0) to be second color
    i1 = 0
    j1 = int(math.floor(pixels_per_unit))
    set_pixel_color(cnf, i1, j1, 1, N, B)
    
    # Constrain third pixel equidistant from first and second with length 1
    i2 = int(math.floor(pixels_per_unit*(math.sqrt(3)/2)))
    j2 = int(math.floor(pixels_per_unit/2))
    set_pixel_color(cnf, i2, j2, 2, N, B)
    
    # For each pair of adjacent pixels, ensure that both are not the same color
    for pair in pairs:
        for k in range(K):
            clause = []
            for b in range(B):
                for i in range(2):
                    clause.append(-1*scale_bit(get_bit(k, b))*pixel_bit_to_int(pair[i], b, N, B))
            cnf.append(clause)
    
    return cnf
    
# Given a satisfying assignment for the formula returned by pairs_to_SAT, this function converts it to a coloring
def solution_to_coloring(solution, N, B, K):
    coloring = [[0 for j in range(N)] for i in range(N)]
    for i in range(N):
        for j in range(N):
            color = 0
            for b in range(B):
                if solution[pixel_bit_to_int((i, j), b, N, B) - 1] > 0:
                    color = set_bit(color, b)
            coloring[i][j] = color     
            
    return coloring

# Given parameters S (side length of square), N (number of pixels on side of square), K (number of colors)
# and wrapping (true if we want pixels to be adjacent accross border of square), this function uses a SAT
# solver and returns a satisfying coloring or "UNSAT" if the problem is not satisfiable
def SAT_solve(S, N, K, wrapping, itersolve=False):
    pairs = pairs_helper.list_of_pixel_pairs(S, N, wrapping, pairs_helper.Format.LIST)
    B = int(math.ceil(math.log(K, 2)))
    cnf = pairs_to_SAT(pairs, S, N, B, K)
    
    solution = []
    if itersolve:
        solution = pycosat.itersolve(cnf)
    else:
        solution = pycosat.solve(cnf)
    if solution == "UNSAT":
        return solution
    
    if itersolve:
        return [solution_to_coloring(sol, N, B, K) for sol in solution]
    else:
        return solution_to_coloring(solution, N, B, K)

# Like SAT_Solve but instead of returning one solution, it returns a list of all solutions
def SAT_itersolve(S, N, K, wrapping):
    return SAT_solve(S, N, K, wrapping, True)