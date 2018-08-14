import matplotlib.pyplot as plt
import discmaker as dm
import numpy as np;
import data
import plotmoser as pm
import matplotlib.cm as cm

fig, axes = plt.subplots(figsize = (6,6))

def createColours():
    x = np.arange(15)
    ys = [i+x+(i*x)**2 for i in range(10)]
    colors = cm.rainbow(np.linspace(0, 1, len(ys)))
    return colors

def createBoldColours(numCol = 15):
    return [[np.random.random() for i in range(4)] for j in range(numCol)]


#Edges
pm.plotmoser(axes)

#Nodes and Discs
colors = createBoldColours()

#Nodes
xvals =[t[0] for t in data.points]
yvals = [t[1] for t in data.points]

#hackey zorder = 10 to stay atop discs
axes.scatter(xvals, yvals, c = colors[:len(yvals)], alpha=1, linewidths=6, zorder=10)

#hackey i to keep same colours as Nodes
for i in range (0, len(xvals)):
    dm.createCircle(axes, x = xvals[i], y = yvals[i],
        delta = data.delta, color = colors[i], a = 0.8)

axes.set_xlim(-2,2)
axes.set_ylim(-2,2)
plt.gca().set_aspect('equal', adjustable = 'box')
plt.show()

