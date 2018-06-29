import numpy
import argparse
import simulated_annealing
import sat_solver
import sat_solver_bits

canUseMatPlotLib = True
try:
    import printColorGrid
except ImportError:
    canUseMatPlotLib = False


# DEFAULT CONSTANTS
S = 4 # Side length of nxn square
N = 20 # Number of pixels on one side of square
K = 7 # Number of colors
INIT_TEMP = 10 # Initial temperature for the simulated annealing algorithm
COOLING_RATE = 0.15 # Cooling rate for the simulated annealing algorithm. Each iteration, T is multiplied by (1-cooling_rate)


parser = argparse.ArgumentParser(description="Find discrete colorings of the plane. If command line arguments not used, the default constants in the .py will be used instead.")

parser.add_argument('--sat', action='store_true', help='use the SAT solver')
parser.add_argument('--sim', action='store_true', help='use simulated annealing. Without this flag the default action is SAT.')
parser.add_argument('-s', '-S', type=float, default=S, help='side length of nxn square')
parser.add_argument('-n', '-N', type=int, default=N, help='number of pixels on one side of square')
parser.add_argument('-k', '-K', type=int, default=K, help='number of colors')
parser.add_argument('--wrapping', '--wrap',  action='store_true', help='Whether or not we wrap distances across edges of square when finding pairs of pixels unit distance from each other')
parser.add_argument('--iter', action='store_true', help='iterate through all solutions for the SAT solver')
parser.add_argument('--bits', action='store_true', help='use SAT solver with bit variales')
parser.add_argument('-t', type=int, default=INIT_TEMP, help='initial temperature for simulated annealing')
parser.add_argument('-cr', type=float, default=COOLING_RATE, help='cooling rate for simulated annealing')
parser.add_argument('--dens', action='store_true', help='include density of color in cost of simulated annealing')
parser.add_argument('--cont', action='store_true', help='reward continuity of color in cost of simulated annealing')
parser.add_argument('--npy', action='store_true', help='store coloring in .npy file instead of png')

args = parser.parse_args()

colorings = []
name = 's' + (str(args.s)).replace('.',',') + '_n' + str(args.n) + '_k' + str(args.k)
if args.wrapping:
    name += '_wrapping'

# SIMULATED ANNEALING
if args.sim:
    name = 'sim_annealing/' + name + '_temp' + str(args.t) + '_cr' + (str(args.cr)).replace('.',',')
    if args.dens:
        name += '_dens'
    if args.cont:
        name += '_cont'
    # use simulated annealing to find an optimal coloring given the parameters
    coloring, cost = simulated_annealing.simulated_annealing(args.s, args.n, args.k, args.wrapping, args.t, args.cr, use_density_cost=args.dens, use_continuity_cost=args.cont)
    colorings.append(coloring)
    
    name += '_cost' + ("{:.2f}".format(cost)).replace('.',',')
    
# SAT SOLVER
else:
    if not args.iter:
        name = 'SAT/' + name
        coloring = None
        if not args.bits:
            coloring = sat_solver.SAT_solve(args.s, args.n, args.k, args.wrapping)
        else:
            name = name + '_bits'
            coloring = sat_solver_bits.SAT_solve(args.s, args.n, args.k, args.wrapping)
        
        if coloring == "UNSAT":
            print "This coloring problem is unsatisfiable."
        else:
            colorings.append(coloring)
            
    else:
        name = 'SAT_iter/' + name + '_iter'
        colorings = sat_solver.SAT_itersolve(args.s, args.n, args.k, args.wrapping)
        if not colorings:
            print "This coloring problem is unsatisfiable."

num_col = 0
for coloring in colorings:
    current_name = name
    if args.iter:
        current_name = current_name + str(num_col)
    if args.npy or not canUseMatPlotLib:
        numpy.save('./colorarrays/' + current_name, coloring)
        print current_name + '.npy saved'
    else:
        printColorGrid.create_coloring(coloring, args.n, args.k, './Colorings/' + current_name)
        print 'Fig saved'
        print current_name
    num_col += 1
