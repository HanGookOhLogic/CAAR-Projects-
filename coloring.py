import numpy
import argparse
import simulated_annealing
import sat_solver
import sat_solver_bits
import integer_programming
import pairs_helper

canUseMPI = True
try:
    from mpi4py import MPI
except ImportError:
    canUseMPI = False
    
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
LENGTH_INCREASE = 1.2

parser = argparse.ArgumentParser(description="Find discrete colorings of the plane. If command line arguments not used, the default constants in the .py will be used instead.")

parser.add_argument('--sat', action='store_true', help='use the SAT solver')
parser.add_argument('--sim', action='store_true', help='use simulated annealing. Without this flag the default action is SAT.')
parser.add_argument('--prog', action='store_true', help='use integer programming')
parser.add_argument('-s', type=float, default=S, help='side length of nxn square')
parser.add_argument('-n', type=int, default=N, help='number of pixels on one side of square')
parser.add_argument('-k', type=int, default=K, help='number of colors')
parser.add_argument('-forb', type=float, default=1, help='second forbidden distance')
parser.add_argument('--wrapping', '--wrap',  action='store_true', help='Whether or not we wrap distances across edges of square when finding pairs of pixels unit distance from each other')
parser.add_argument('--circ', action='store_true', help='circle bound instead of square')
parser.add_argument('--annu', action='store_true', help='annulus bound instead of square')
parser.add_argument('--iter', action='store_true', help='iterate through all solutions for the SAT solver')
parser.add_argument('--bits', action='store_true', help='use SAT solver with bit variales')
parser.add_argument('-t', type=int, default=INIT_TEMP, help='initial temperature for simulated annealing')
parser.add_argument('-cr', type=float, default=COOLING_RATE, help='cooling rate for simulated annealing')
parser.add_argument('-li', type=float, default=LENGTH_INCREASE, help='length increase rate for repetition schedule of simulated annealing')
parser.add_argument('--dens', action='store_true', help='include density of color in cost of simulated annealing')
parser.add_argument('--cont', action='store_true', help='reward continuity of color in cost of simulated annealing')
parser.add_argument('--npy', action='store_true', help='store coloring in .npy file instead of png')

args = parser.parse_args()

colorings = []
name = 's' + (str(args.s)).replace('.',',') + '_n' + str(args.n) + '_k' + str(args.k)
if args.wrapping:
    name += '_wrapping'
    
if args.annu:
    args.circ = True
    name += '_annulus'
elif args.circ:
    name += '_circle'

if args.forb != 1:
    name += '_forb' + (str(args.forb)).replace('.',',')
    
# SIMULATED ANNEALING
if args.sim:
    name = 'sim_annealing/' + name + '_temp' + str(args.t) + '_cr' + (str(args.cr)).replace('.',',')
    if args.dens:
        name += '_dens'
    if args.cont:
        name += '_cont'
    # use simulated annealing to find an optimal coloring given the parameters
    coloring, cost = simulated_annealing.simulated_annealing(args)
    colorings.append(coloring)
    
    name += '_cost' + ("{:.2f}".format(cost)).replace('.',',')

elif args.prog:
    name = 'programming/' + name
    coloring, cost = integer_programming.relaxed_integer_programming(args)
    colorings.append(coloring)
    name += '_cost' + str(cost)
    
# SAT SOLVER
else:
    if not args.iter:
        name = 'SAT/' + name
        coloring = None
        if not args.bits:
            coloring = sat_solver.SAT_solve(args)
        else:
            name = name + '_bits'
            coloring = sat_solver_bits.SAT_solve(args)
        
        if coloring == "UNSAT":
            print "This coloring problem is unsatisfiable."
        else:
            colorings.append(coloring)
            
    else:
        name = 'SAT_iter/' + name + '_iter'
        colorings = sat_solver.SAT_itersolve(args)
        if not colorings:
            print "This coloring problem is unsatisfiable."

if canUseMPI:
    colorings = MPI.COMM_WORLD.reduce(colorings)
    
num_col = 0
for coloring in colorings:
    if args.circ:
        pairs_helper.circle_helper(coloring, args.s, args.n, args.annu)
        
    current_name = name
    if args.iter:
        current_name = current_name + str(num_col)
    if args.npy or not canUseMatPlotLib:
        numpy.save('./colorarrays/' + current_name, coloring)
        print current_name + '.npy saved'
    else:
        printColorGrid.create_coloring(coloring, args.n, 10, './Colorings/' + current_name)
        print 'Fig saved'
        print current_name
    num_col += 1
