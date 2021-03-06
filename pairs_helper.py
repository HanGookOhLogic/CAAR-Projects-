import math
from enum import Enum

# Format enum class which specifies which format the list of pairs data structure is returned as
class Format(Enum):
    LIST = 1
    MATRIX = 2

def in_circ(point, s, n, annulus=False):
    center_length = float(s)/2
    pixel_length = float(s)/n
    
    dist = 0
    for i in range(1):
        for j in range(1):
            x = (point[0]+i)*pixel_length
            y = (point[1]+j)*pixel_length
            new_dist = math.hypot(x - center_length, y - center_length)
            if new_dist > dist:
                dist = new_dist
    
    circle_radius = center_length
    if annulus:
        circle_radius = 0.5
    
    if dist <= circle_radius:
        return True
    else:
        return False    

# adds a pair of adjacent pixels to the pairs data structure depending on format specified
def add_pair(pairs, x1, y1, x2, y2, args, format):
    if args.circ and not (in_circ((x1, y1), args.s, args.n) and in_circ((x2, y2), args.s, args.n)):
        return
    if args.annu and (in_circ((x1, y1), args.s, args.n, True) or in_circ((x2, y2), args.s, args.n, True)):
        return
    
    if format == Format.LIST:
        pairs.append(((x1, y1), (x2, y2)))
    elif format == Format.MATRIX:
        pairs[x1][y1].append((x2, y2))
        pairs[x2][y2].append((x1, y1))
    return 
    
# Generates a list of pairs of pixels containing points a distance of 1 from each other
# Input: s - length of side of grid of pixels
#        n - number of pixels on each side of grid (nxn grid)
#        wrapping - set to true if we want distances to wrap across edges of grid as if grid was tiled
#        list_format - set to true if you want the function to return 
def list_of_pixel_pairs(args, format=Format.MATRIX):
    pairs = None
    if format == Format.LIST:
        pairs = []
    elif format == Format.MATRIX:
        pairs = [[[] for i in range(args.n)] for j in range(args.n)] # nxn array of lists of points distance 1 from each pixel
        
    pixel_length = float(args.s)/args.n # length of each pixel
  
    max_forb_dist = max(1, args.forb)
    for i in range(0, int(max_forb_dist*math.ceil(float(args.n)/args.s + 1))):
        for j in range(0, int(math.ceil(float(args.n)/args.s + 1))):
            min_dist = 0
            max_dist = 0
            # calculate the minimum and maximum distance between a point in pixel (0, 0) and pixel (s/n*i, s/n*j)
            if i == 0:
                min_dist = pixel_length*(j-1)
                max_dist = pixel_length*(j+1)
            elif j == 0:
                min_dist = pixel_length*(i-1)
                max_dist = pixel_length*(i+1)
            else:
                min_dist = math.hypot(pixel_length*(i-1), pixel_length*(j-1))
                max_dist = math.hypot(pixel_length*(i+1), pixel_length*(j+1))
            
            # if 1 is between the distances, then by continuity, there is a pair of points a distance of 1 in this pair of pixels
            if (min_dist < 1 and 1 <= max_dist) or (min_dist < args.forb and args.forb <= max_dist):
                # by symmetry of our pixel division, the pixel pair we found can be applied to any starting pixel, not just (0,0) and we can flip the pair vertically and horizontally as well
                for x in range(args.n):
                    for y in range(args.n):
                        if args.wrapping:
                            add_pair(pairs, x, y, (x+i)%n, (y+j)%n, args, format)
                            if i != 0 and j != 0:
                                add_pair(pairs, x, y, (x-i)%n, (y+j)%n, args, format)
                        else:
                            if y + j < args.n:
                                if x + i < args.n:
                                    add_pair(pairs, x, y, x+i, y+j, args, format)
                                if x - i >= 0 and i != 0 and j != 0:
                                    add_pair(pairs, x, y, x-i, y+j, args, format)
    return pairs
    
def circle_helper(coloring, s, n, annulus=False):
    for x in range(n):
        for y in range(n):
            if not in_circ((x, y), s, n):
                coloring[x][y] = 9
            if annulus and in_circ((x, y), s, n, True):
                coloring[x][y] = 9