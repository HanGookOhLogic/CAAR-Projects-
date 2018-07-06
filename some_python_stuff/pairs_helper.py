import math
from enum import Enum

# Format enum class which specifies which format the list of pairs data structure is returned as
class Format(Enum):
    LIST = 1
    MATRIX = 2

# adds a pair of adjacent pixels to the pairs data structure depending on format specified
def add_pair(pairs, x1, y1, x2, y2, format):
    if format == Format.LIST:
        pairs.append(((x1, y1), (x2, y2)))
    elif format == Format.MATRIX:
        pairs[x1][y1].append((x2, y2))
        pairs[x2][y2].append((x1, y1))
        
# Generates a list of pairs of pixels containing points a distance of 1 from each other
# Input: s - length of side of grid of pixels
#        n - number of pixels on each side of grid (nxn grid)
#        wrapping - set to true if we want distances to wrap across edges of grid as if grid was tiled
#        list_format - set to true if you want the function to return 
def list_of_pixel_pairs(s, n, wrapping):
    pairs = []
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
            if min_dist <= 1 and 1 <= max_dist:
                # by symmetry of our pixel division, the pixel pair we found can be applied to any starting pixel, not just (0,0) and we can flip the pair vertically and horizontally as well
                for x in range(n):
                    for y in range(n):
                        if wrapping:
                            add_pair(pairs, x, y, (x+i)%n, (y+j)%n, Format.MATRIX)
                            if i != 0 and j != 0:
                                add_pair(pairs, x, y, (x-i)%n, (y+j)%n, Format.MATRIX)
                        else:
                            if y + j < n:
                                if x + i < n:
                                    add_pair(pairs, x, y, x+i, y+j, Format.MATRIX)
                                if x - i >= 0 and i != 0 and j != 0:
                                    add_pair(pairs, x, y, x-i, y+j, Format.MATRIX)
                    
    return pairs






def rect_pixel_pairs(w, h, r, c, wrapping):
    pairs = []
    pairs = [[[] for i in range(c)] for j in range(r)] # nxn array of lists of points distance 1 from each pixel
    
    pixel_width = float(h)/r
    pixel_height = float(w)/c
  
    for i in range(0, int(math.ceil(float(r)/h + 1))):
        for j in range(0, int(math.ceil(float(c)/w + 1))):
            min_dist = 0
            max_dist = 0
            # calculate the minimum and maximum distance between a point in pixel (0, 0) and pixel (s/n*i, s/n*j)
            if i == 0:
                min_dist = pixel_width*(j-1)
                max_dist = pixel_width*(j+1)
            elif j == 0:
                min_dist = pixel_height*(i-1)
                max_dist = pixel_height*(i+1)
            else:
                min_dist = math.hypot(pixel_height*(i-1), pixel_width*(j-1))
                max_dist = math.hypot(pixel_height*(i+1), pixel_width*(j+1))
        
            # if 1 is between the distances, then by continuity, there is a pair of points a distance of 1 in this pair of pixels
            if min_dist <= 1 and 1 <= max_dist:
                # by symmetry of our pixel division, the pixel pair we found can be applied to any starting pixel, not just (0,0) and we can flip the pair vertically and horizontally as well
                for x in range(r):
                    for y in range(c):
                        if wrapping:
                            add_pair(pairs, x, y, (x+i)%r, (y+j)%c, Format.MATRIX)
                            if i != 0 and j != 0:
                                add_pair(pairs, x, y, (x-i)%r, (y+j)%c, Format.MATRIX)
                        else:
                            if y + j < c:
                                if x + i < r:
                                    add_pair(pairs, x, y, x+i, y+j, Format.MATRIX)
                                if x - i >= 0 and i != 0 and j != 0:
                                    add_pair(pairs, x, y, x-i, y+j, Format.MATRIX)
                    
    return pairs

def check():
    l1 = rect_pixel_pairs(5,5,120,120,True)
    l2 = list_of_pixel_pairs(5,120,True)
    print(l1==l2)
