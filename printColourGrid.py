import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

def create_coloring(data, size, numCol=7):
    #scalar to RGBA mapping
    #Colormap object generated from a list of colors, colormap is a mapping from numbers to colours
    cmap = colors.ListedColormap(['red', 'blue', 'yellow','green','purple','orange','pink','black','white','brown'])

    #Generate a colormap index based on discrete intervals. This essentially normalize the colormap's mapping
    #to map from integers (our data) to colours
    bounds = np.arange(numCol + 1)
    norm = colors.BoundaryNorm(bounds, cmap.N)

    #return gets us fig, which we ignore. returns axes
    fig, ax = plt.subplots()

    #data = np.random.rand(10,10)
    print(data)
    ax.imshow(data, cmap=cmap, norm=norm)

    # draw axis
    ax.xaxis.set_ticks_position('top')
    ax.set_xticks(np.arange(0, size, 1))
    ax.set_yticks(np.arange(0, size, 1))
    #set font size of axis labels
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=5)
    # make a color bar
##  zvals = np.random.rand(100,100)*10-5
##  img = plt.imshow(zvals,interpolation='nearest', cmap = cmap,norm=norm)
##  plt.colorbar(img,cmap=cmap,
##  norm=norm,boundaries=bounds,ticks=[-5,0,5])
##
    plt.show()