import numpy 
from matplotlib import pyplot as plt
import data

def plotmoser(axes): 
    points = numpy.array([[1,2],[4,5],[2,7],[3,9],[9,2]])
    edges = numpy.array([[0,1],[3,4],[3,2],[2,4]])
    
    x = points[:,0].flatten()
    y = points[:,1].flatten()
    lines = numpy.array(data.edges).T
    
    
    xes = lines[0]
    yes = lines[1]
    
    xlist = [None]
    ylist = [None]
    #ax, bx, NONE
    for x in range (0, len(xes[0])):
        print(xes[0][x])
        xlist = numpy.append(xlist, xes[0][x])
        xlist = numpy.append(xlist, xes[1][x])
        xlist = numpy.append(xlist, None)
    for y in range (0, len(yes[0])):
        ylist = numpy.append(ylist, yes[0][y])
        ylist = numpy.append(ylist, yes[1][y])
        ylist = numpy.append(ylist, None)
    
    axes.plot(xlist, ylist)
    
