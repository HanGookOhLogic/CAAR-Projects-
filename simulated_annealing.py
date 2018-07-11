import math
import random
import copy
import pairs_helper  
  
# calculates the cost of an assignment, i.e. the number of pairs of monochromatic adjacent pixels
def total_cost(pairs, assignment, n):
    total_cost = 0
    for i in range(n):
        for j in range(n):
            neighboring_pixels = pairs[i][j]
            current_color = assignment[i][j]
            for pixel in neighboring_pixels:
                if current_color == assignment[pixel[0]][pixel[1]]:
                    total_cost += 1
    return total_cost / 2
	
# calculates the change in cost of an assignment where pixel 'new_pixel' is changed to color 'new_color'
# if input includes old_cost, the cost of the assignment before the change, cost will return the total new cost
def relative_cost(pairs, assignment, n, new_pixel, new_color, old_cost=0):
    prev_cost = 0
    new_cost = 0
    old_color = assignment[new_pixel[0]][new_pixel[1]]
    neighboring_pixels = pairs[new_pixel[0]][new_pixel[1]]
    for pixel in neighboring_pixels:
        current_color = assignment[pixel[0]][pixel[1]]
        if current_color == new_color:
            new_cost += 1
        if current_color == old_color:
            prev_cost += 1
    return old_cost + (new_cost - prev_cost)

def find_first_color_frequency(assignment, n):
    frequency = 0
    for i in range(n):
        for j in range(n):
            if assignment[i][j] == 0:
                frequency += 1
    return frequency
    
def total_density_cost(first_color_frequency, n):
    return float(first_color_frequency) / (n*n)
    
def relative_density_cost(old_color, new_color, n):
    if old_color == 0:
        return float(-1)/(n*n)
    elif new_color == 0:
        return float(1)/(n*n)
    else:
        return 0

def relative_continuity_cost(assignment, new_pixel, new_color, n, wrapping):
    cost = 0
    old_color = assignment[new_pixel[0]][new_pixel[1]]
    for i in range(new_pixel[0] - 1, new_pixel[0] + 2):
        for j in range(new_pixel[0] - 1, new_pixel[0] + 2):
            if not (i == 0 and j == 0):
                if wrapping or (i >= 0 and i < n and j >= 0 and j < n):
                    current_color = assignment[i][j]
                    if current_color != old_color:
                        cost -= 1
                    if current_color != new_color:
                        cost += 1
    return cost
# generates a random assignment of colors to pixels
def random_assignment(k, n):
    return [[random.randrange(k) for i in range(n)] for j in range(n)]
  
# given an assignment, it finds a neighboring assignment by randomly flipping the color of one pixel
# returns new assignment, coordinates of changed pixel, and its old color
def neighboring_solution(assignment, n, k):
    random_pixel = (random.randrange(n), random.randrange(n))
    old_color = assignment[random_pixel[0]][random_pixel[1]]
    new_color = random.choice(range(old_color) + range(old_color + 1, k))
    return random_pixel, new_color
  
# changes the color of pixel in assignment to color
def change_pixel(assignment, pixel, color):
    assignment[pixel[0]][pixel[1]] = color
  
# Simulated annealing algorithm to find a coloring of an nxn grid of pixels with side length s and number of colors k with a globally minimum number of pairs of same colored pixels that are distance 1 from each other. 
# T_initial - the starting temperature
# cooling_rate - Each iteration, the temperature is multiplied by (1-cooling_rate). The bigger the cooling rate, the faster T converges to 0.
# final_temp - the temperature T must decrease to before algorithm terminates
# length_initial - number of repetitions for temperature T_initial
# length_increase - the number of repetitions for each temperature is multiplied by length_increase each time we decrease the temperature. So if length_increase is higher, the algorithm will take longer but try more options.
# use_density_cost - set to True to include the density of the first color in the cost function (useful if we want to try to decrease the occurence of a color as much as possible)
# density_scale - how much weight the density of the first color has in the cost
# use_continuity_cost - set to True to reward continuity of colors in the cost function
# continuity_scale - how much weight continuity has in the cost
def simulated_annealing(s, n, k, wrapping=False, circle=False, annulus=False, T_initial=10, cooling_rate=0.15, final_temp=0.05, length_initial=100, length_increase=1.2, use_density_cost=False, density_scale=1, use_continuity_cost=False, continuity_scale=0.25):
    pairs = pairs_helper.list_of_pixel_pairs(s, n, wrapping, pairs_helper.Format.MATRIX, circle, annulus)
    current_assignment = random_assignment(k, n)
    current_cost = total_cost(pairs, current_assignment, n)
    
    if use_density_cost:
        first_color_frequency = find_first_color_frequency(current_assignment, n)
        current_cost += density_scale*total_density_cost(first_color_frequency, n)
        
    
    T = T_initial
    length = length_initial
    while T > final_temp and current_cost > 0:
        iter = 0
        while iter < length:
            new_pixel, new_color = neighboring_solution(current_assignment, n, k)
            change_in_cost = relative_cost(pairs, current_assignment, n, new_pixel, new_color)
            if use_density_cost:
                change_in_cost += density_scale*relative_density_cost(current_assignment[new_pixel[0]][new_pixel[1]], new_color, n)
                
            continuity_factor = 0
            if use_continuity_cost:
                continuity_factor = (continuity_scale/k)*relative_continuity_cost(current_assignment, new_pixel, new_color, n, wrapping)
            if change_in_cost + continuity_factor <= 0:
                change_pixel(current_assignment, new_pixel, new_color)
                current_cost += change_in_cost
            else:
                Metropolis_probability = math.exp(-1*(change_in_cost + continuity_factor)/T)
                if Metropolis_probability > random.uniform(0,1):
                    change_pixel(current_assignment, new_pixel, new_color)
                    current_cost += change_in_cost
            iter += 1
        T = T*(1-cooling_rate)
        length *= length_increase
    return current_assignment, current_cost
