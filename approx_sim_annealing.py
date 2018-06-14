import random
import math


def update_temperatureT(T):
    return T - 1

def update_temperatureR(R):
    return R + 1

def randomPoint(colSize, rowSize):
    return (random.randint(0, colSize + 1) random.randint(0, rowSize + 1))

def randomColor(numColors):
    ##choose randomly from a list of string colours


#allPairs is a nxnxm where allPairs[i,j]: 1-dimensional array containing
#pixels distance 1 from the the pixel (i,j)

#currentColouring is an nxn list where each entry the colour
#of that corresponding grid

#check with Dan that the col,row is the same at the pix0, pix1!

#returns a list
#index 0 number of total collisions recorded across the board
#the rest are a list of tuples (pixel, #ofcollisions per that pixel)

def cost_Board(allPairs, currentColoring):
    totalCostOfColoring = 0
    costOfColouring = 0
    invalidPixels = [0]
    for column in allPairs:
        for row in column:
            for pixel in row:
                costOfColouring = 0
                if(currentColoring[column, row] == currentColoring[pixel[0],pixel[1]]):
                    costOfColoring = costOfColoring + 1
                    totalCostOfColoring = totalCostOfColoring + costOfColoring
                    invalidPixels.append((pixel,costOfColoring))
    invalidPixels[0] = totalCostOfColouring
    totalPackage = (invalidPixels)
    return totalPackage

#calculates the cost of changing the color of one pixel
def cost_local(pairList, currentColoring, color):
    totalCost = 0
    for point in pairList:
        if(currentColoring[pair[0]][pair[1]] == color):
            totalCost = totalCost + 1
    return totalCost


#currentColoring is the graph

##TODO: Find a way to save the current cost in the point as your find it along with the color. 
def approx_simulated_annealing_rp_rc(currentColoring, numColors):
    T = 45
    while(T < 1):
        ##DAN WILL DO THIS
        allpair = generateAllPairs(currentColoring)
        
        point = randomPoint(len(currentColoring), len(currentColoring[0]))
        
        #the x,y of the point is the location of the point in the nxnxm allpair list
        #Calculates the collision number of the current coloring for this point
        #(list of lists, list list with colors, string as a color) 
        orig_cost = cost_local(allpair[point[0]][point[1]], currentColoring, currentColoring[point[0]][point[1]])

        #Calculates the collision number of a random color (maybe do for loop and choose from those?)
        color = randomColor(numColors)
        #ensures a new color is tried 
        while (currentColoring[pair[0]][pair[1]] = color):
            color = randomColor(numColors)
            
        after_cost = cost_local(allpair[point[0]][point[1]], currentColoring, color)

        if(after_cost < orig_cost):
            currentColoring[pair[0]][pair[1]] = color
        else if (math.math.exp((orig_cost - after_cost)/T) > random.random()):
            currentColoring[pair[0]][pair[1]] = color
        T = T - 1

        
    
    

    










                    
                    


