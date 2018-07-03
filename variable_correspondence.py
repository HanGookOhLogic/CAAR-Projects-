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