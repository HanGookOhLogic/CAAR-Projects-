from pulp import *
from variable_correspondence import *
import pairs_helper

def create_problem(pairs, N, K):
    prob = LpProblem("Coloring", LpMaximize)
    lpVars = [LpVariable(i, 0, 1) for i in range(number_of_variables(N,K))]
    
    # objective function
    prob += sum(lpVars)
    
    prob += lpVars[0] == 1
    
    # enforce color chosen
    for i in range(N):
        for j in range(N):
            constraints = 0
            for k in range(K):
                constraints += lpVars[pixel_color_to_int((i, j), k, N, K) - 1]
            prob += constraints == 1
    
    # enforce pairs
    for pair in pairs:
        for k in range(K):
            constraints = 0
            for i in range(2):
                constraints += lpVars[pixel_color_to_int(pair[i], k, N, K) - 1]
            prob += constraints <= 1
    
    return prob, lpVars
    
def solution_to_coloring(prob, lpVars, N, K):
    col = [[0 for i in range(N)] for j in range(N)]
    for i in range(N):
        for j in range(N):
            max_val = 0
            max_col = 0
            for k in range(K):
                current_val = lpVars[pixel_color_to_int((i, j), k, N, K) - 1].varValue
                if current_val >= max_val:
                    max_val = current_val
                    max_col = k
            col[i][j] = k
    return col
    
def total_cost(coloring, pairs):
    cost = 0
    for pair in pairs:
        if coloring[pair[0][0]][pair[0][1]] == coloring[pair[1][0]][pair[1][1]]:
            cost += 1
    return cost
    
def relaxed_integer_programming(S, N, K, wrapping=False, circle=False, annulus=False):
    pairs = pairs_helper.list_of_pixel_pairs(S, N, wrapping, pairs_helper.Format.LIST, circle, annulus)
    
    prob, lpVars = create_problem(pairs, N, K)
    prob.solve()
    print LpStatus[prob.status]
    coloring = solution_to_coloring(prob, lpVars, N, K)
    cost = total_cost(coloring, pairs)
    return coloring, cost