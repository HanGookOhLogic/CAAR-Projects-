import pycosat
import pairs_helper

def pixel_color_to_int(p, k, N, K):
    return (N*p[0] + p[1])*K + k + 1
    
def int_to_pixel_color(sat_var, N, K):
    square = (sat_var - 1) / K
    i = square / N
    j = square % N
    k = (sat_var - 1) % K
    return (i, j), k
    
def number_of_variables(N, K):
    return N*N*K

def pairs_to_SAT(pairs, N, K):
    cnf = []
    for i in range(N):
        for j in range(N):
            clause = []
            for k in range(K):
                clause.append(pixel_color_to_int((i, j), k, N, K))
            cnf.append(clause)
    
    for pair in pairs:
        for k in range(K):
            cnf.append([-1*pixel_color_to_int(pair[0], k, N, K), -1*pixel_color_to_int(pair[1], k, N, K)])
    
    return cnf
	
def solution_to_coloring(solution, N, K):
    coloring = [[0 for j in range(N)] for i in range(N)]
    num_var = number_of_variables(N, K)
    for sat_var in range(num_var):
        if solution[sat_var] > 0:
            pixel, k = int_to_pixel_color(sat_var + 1, N, K)
            coloring[pixel[0]][pixel[1]] = k
    return coloring

def SAT_solve(S, N, K, wrapping):
    pairs = pairs_helper.list_of_pixel_pairs(S, N, wrapping, pairs_helper.Format.LIST)
    cnf = pairs_to_SAT(pairs, N, K)
    solution = pycosat.solve(cnf)
    if solution == "UNSAT":
        return solution
    return solution_to_coloring(solution, N, K)