import math
import random
import copy
import printColourGrid
# CONSTANTS
S = 2; # Side length of nxn square
N = 20; # Number of pixels on one side of square
K = 10; # Number of colors
WRAPPING = False; # Whether or not we wrap distances across edges of square when finding pairs of pixels unit distaqnce from each other

def list_of_pixel_pairs(s, n, wrapping):
  pairs = [[[] for i in range(n)] for j in range(n)]; # nxn array of lists of points distance 1 from each pixel
  pixel_length = float(s)/n; # length of each pixel

  for i in range(0, int(math.ceil(float(n)/s + 1))):
    for j in range(0, int(math.ceil(float(n)/s + 1))):
      min_dist = 0;
      max_dist = 0;
      # calculate the minimum and maximum distance between a point in pixel (0, 0) and pixel (s/n*i, s/n*j)
      if i == 0:
        min_dist = pixel_length*(j-1);
        max_dist = pixel_length*(j+1);
      elif j == 0:
        min_dist = pixel_length*(i-1);
        max_dist = pixel_length*(i+1);
      else:
        min_dist = math.hypot(pixel_length*(i-1), pixel_length*(j-1));
        max_dist = math.hypot(pixel_length*(i+1), pixel_length*(j+1));

      # if 1 is between the distances, then by continuity, there is a pair of points a distance of 1 in this pair of pixels
      if min_dist <= 1 and 1 <= max_dist:
        # by symmetry of our pixel division, the pixel pair we found can be applied to any starting pixel, not just (0,0) and we can flip the pair vertically and horizontally as well
        for x in range(n):
          for y in range(n):
            if wrapping:
              pairs[x][y].append(((x+i)%n, (y+j)%n));
              pairs[(x+i)%n][(y+j)%n].append((x, y));
              if i != 0 and j != 0:
                pairs[x][y].append(((x-i)%n, (y+j)%n));
                pairs[(x-i)%n][(y+j)%n].append((x, y));
            else:
              if y + j < n:
                if x + i < n:
                  pairs[x][y].append((x+i, y+j));
                  pairs[x+i][y+j].append((x, y));
                if x - i >= 0 and i != 0 and j != 0:
                  pairs[x][y].append((x-i, y+j));
                  pairs[x-i][y+j].append((x, y));
  
  return pairs;


# calculates the cost of an assignment
# if input is just pairs and assignment, cost will iterate through every pair and find total cost
# if input includes new_pixel, a single pixel changed from a previous assignment, and old_color, the color that pixel was changed from, then cost will return the change in cost made by this change in color
# if input includes old_cost, the cost of the assignment before the change, cost will return the total new cost
def cost(pairs, assignment, n, new_pixel=None, new_color=None, old_cost=0):
  total_cost = 0;
  if new_pixel == None or new_color == None:
    for i in range(n):
      for j in range(n):
        neighboring_pixels = pairs[i][j];
        current_color = assignment[i][j];
        for pixel in neighboring_pixels:
          if current_color == assignment[pixel[0]][pixel[1]]:
            total_cost += 1;
    total_cost /= 2;
  else:
    prev_cost = 0;
    new_cost = 0;
    old_color = assignment[new_pixel[0]][new_pixel[1]];
    neighboring_pixels = pairs[new_pixel[0]][new_pixel[1]];
    for pixel in neighboring_pixels:
      current_color = assignment[pixel[0]][pixel[1]];
      if current_color == new_color:
        new_cost += 1;
      if current_color == old_color:
        prev_cost += 1;
    total_cost = old_cost + (new_cost - prev_cost);

  return total_cost;
      
"""
# input pairs refers to a one-dimensional array of pixels a distance one from a given pixel
def visualize_pairs(pairs, n):
  board = [['_' for i in range(n)] for j in range(n)];
  for p in pairs:
    board[p[0]][p[1]] = 'X';

  display = '   ';
  for i in range(n):
    display += str(i % 10) + ' ';
  display += '\n';

  for i in range(n):
    display += str(i % 10) + '  ';
    for j in range(n):
      display += board[i][j] + ' ';
    display += '\n';
  print display;


# input colors is nxn array of colors
def visualize_colors(colors, n):

  display = '   ';
  for i in range(n):
    display += str(i % 10) + ' ';
  display += '\n';

  for i in range(n):
    display += str(i % 10) + '  ';
    for j in range(n):
      display += str(colors[i][j]) + ' ';
    display += '\n';
  print display;
"""
# generates a random assignment of colors to pixels
def random_assignment(k, n):
  return [[random.randrange(k) for i in range(n)] for j in range(n)];

# given an assignment, it finds a neighboring assignment by randomly flipping the color of one pixel
# returns new assignment, coordinates of changed pixel, and its old color
def neighboring_solution(assignment, n):
  random_pixel = (random.randrange(N), random.randrange(N));
  old_color = assignment[random_pixel[0]][random_pixel[1]];
  new_color = random.choice(range(old_color) + range(old_color + 1, K));
  return random_pixel, new_color;

def change_pixel(assignment, pixel, color):
  assignment[pixel[0]][pixel[1]] = color;
  return;

def simulated_annealing(T0=10, cooling_rate=0.15, final_temp=0.05, length_increase=1.2):
  pairs = list_of_pixel_pairs(S, N, WRAPPING);
  current_assignment = random_assignment(K, N);
  T = T0;
  length = 100;
  while T > final_temp:
    length *= length_increase;
    #print length;
    test = True;
    change1 = 0;
    change2 = 0;
    for i in range(int(math.ceil(length))):
      new_pixel, new_color = neighboring_solution(current_assignment, N);
      change_in_cost = cost(pairs, current_assignment, N, new_pixel, new_color);
      if change_in_cost <= 0:
        change_pixel(current_assignment, new_pixel, new_color);
        change1 +=1;
      else:
        Metropolis_probability = math.exp(-1*change_in_cost/T);
        if test:
          #print Metropolis_probability;
          test = False;
        if Metropolis_probability > random.uniform(0,1):
          change_pixel(current_assignment, new_pixel, new_color);
          change2 += 1;
    T = T*(1-cooling_rate);
    visualize_colors(current_assignment, N);
    #print cost(pairs, current_assignment, N);
    #print change1;
    #print change2;
    #print '\n';
  return current_assignment, cost(pairs, current_assignment, N);



a, c = simulated_annealing();
#visualize_colors(a, N);
print( c);
create_coloring(a, N, K);


"""
a = random_assignment(K,N);
visualize_colors(a, N);
nc, np, oc = neighboring_solution(a,N);
visualize_colors(a, N);
visualize_colors(nc,N);
print np;
print oc;
"""

"""
count = 0;
for i in range(100000):
  if random.uniform(0,1) < 5e-20:
    count += 1;
print count;
"""

"""
p = list_of_pixel_pairs(S,N,WRAPPING);
visualize_pairs(p[0][0], N);
a = random_assignment(K, N);
visualize_colors(a, N);

print cost(p, a, N);

rp = (random.randrange(N), random.randrange(N));
oc = a[rp[0]][rp[1]];
nc = random.randrange(K);
a[rp[0]][rp[1]] = nc;
print 'change pixel ' + str(rp) + ' to ' + str(nc);
visualize_colors(a, N);
print cost(p, a, N, rp, oc);
"""
