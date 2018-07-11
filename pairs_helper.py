import math
from enum import Enum

# Format enum class which specifies which format the list of pairs data structure is returned as
class Format(Enum):
    LIST = 1
    MATRIX = 2

def in_circ(point, s, n, annulus=False):
    center_length = 0.5
    if not annulus:
        center_length = float(s)/2
    pixel_length = float(s)/n
    x = (point[0]+0.5)*pixel_length
    y = (point[1]+0.5)*pixel_length
    dist = math.hypot(x - center_length, y - center_length)
    if dist <= center_length:
        return True
    else:
        return False    

# adds a pair of adjacent pixels to the pairs data structure depending on format specified
def add_pair(pairs, x1, y1, x2, y2, s, n, format, circle, annulus):
    if circle and not (in_circ((x1, y1), s, n) and in_circ((x2, y2), s, n)):
        return
    if annulus and (in_circ((x1, y1), s, n, True) or in_circ((x2, y2), s, n, True)):
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
def list_of_pixel_pairs(s, n, wrapping=False, format=Format.MATRIX, circle=False, annulus=False):
    pairs = None
    if format == Format.LIST:
        pairs = []
    elif format == Format.MATRIX:
        pairs = [[[] for i in range(n)] for j in range(n)] # nxn array of lists of points distance 1 from each pixel
        
    pixel_length = float(s)/n # length of each pixel
  
    for i in range(0, int(math.ceil(float(n)/s + 1))):
        for j in range(0, int(math.ceil(float(n)/s + 1))):
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
            if min_dist < 1 and 1 <= max_dist:
                # by symmetry of our pixel division, the pixel pair we found can be applied to any starting pixel, not just (0,0) and we can flip the pair vertically and horizontally as well
                for x in range(n):
                    for y in range(n):
                        if wrapping:
                            add_pair(pairs, x, y, (x+i)%n, (y+j)%n, s, n, format, circle, annulus)
                            if i != 0 and j != 0:
                                add_pair(pairs, x, y, (x-i)%n, (y+j)%n, s, n, format, circle, annulus)
                        else:
                            if y + j < n:
                                if x + i < n:
                                    add_pair(pairs, x, y, x+i, y+j, s, n, format, circle, annulus)
                                if x - i >= 0 and i != 0 and j != 0:
                                    add_pair(pairs, x, y, x-i, y+j, s, n, format, circle, annulus)
                    
    return pairs
    
def circle_helper(coloring, s, n, annulus=False):
    center_length = float(s)/2
    pixel_length = float(s)/n
    for i in range(n):
        for j in range(n):
            x = (i+0.5)*pixel_length
            y = (j+0.5)*pixel_length
            dist = math.hypot(x - center_length, y - center_length)
            if dist > center_length:
                coloring[i][j] = 9
            if annulus and dist <= 0.5:
                coloring[i][j] = 9