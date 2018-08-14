import numpy as np
import matplotlib.pyplot as plt
import data
import pylab as pl
from matplotlib import collections as mc
from matplotlib import cm as cm
points = np.array([[0,0], [0,1], [0,3]])
#
#x = points[:,0]
#y = points[:,1]
#mess = points[:,:]
#
##ILLEGAL: karma = numpy.array([ [67,68], [ [0,0], [1,1]]])
#
#flatmess = mess.flatten()
#print(x)
#print(y)
#print(mess)
#
#
#x = np.arange(10)
#ys = [i+x+(i*x)**2 for i in range(10)]
#colors = cm.rainbow(np.linspace(0, 1, len(ys)))
#xvals =[t[0] for t in data.points]
#yvals = [t[1] for t in data.points]
#plt.scatter(xvals, yvals, c = colors[:len(yvals)], alpha=1, linewidths=6)

xes = np.linspace(0, 2*np.pi, 400)
yes = np.sin(xes**2)
fig, (ax1, ax2) = plt.subplots(1,2,sharey=True)
ax1.plot(xes,yes)
ax2.scatter(xes,yes)
plt.show()