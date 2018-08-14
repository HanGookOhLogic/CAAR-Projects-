import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def createCircle(ax, x=0,y=0, delta=0, color = (0,0.8,0.8), a = 0.1):
    print(color)
    idel = int(delta * 100)
    jump = int((delta/10)*100)
    
    if jump <= 0:
        jump = 1
    for delt in range (-idel - 1, idel + 1, jump):
       circ = patches.Circle((x,y), 1 + delt/100, edgecolor=color, facecolor='none',alpha=a, lw=6)
       ax.add_patch(circ)
       






#from matplotlib import collections  as mc

''' xlist = np.linspace(-2.0, 1.0, 100)    # Create 1-D arrays for x,y dimensions
ylist = np.linspace(-1.0, 2.0, 100)
X,Y = np.meshgrid(xlist, ylist)        # Create 2-D grid xlist,ylist values
Z = np.sqrt(X*0 + 0.1)               # Compute function values on the grid
plt.contour(X, Y, Z, [0.5, 1.0, 1.2, 1.5], colors = 'k', linestyles = 'solid', linewidths=4.0)
plt.axes().set_aspect('equal')         # Scale the plot size to get same aspect ratio
plt.axis([-1.0, 1.0, -0.5, 0.5])       # Change axis limits
plt.show()
 '''

#linewidth 100 = 2 units
#eps = 0.1
#fig1 = plt.figure()
#ax1 = fig1.add_subplot(111, aspect = 'equal')
#ax1.set_xlim(-20, 20)
#ax1.set_ylim(-20, 20)
#x_large = np.arange(0,1 + eps,0.01)
#x_small = np.arange(0, 1- eps, 0.01)
#y_large = np.sqrt((1 + eps)**2 - (x_large**2))
#y_small = np.sqrt((1 - eps)**2 - (x_small**2))
#result = np.zeros(y_large.shape)
#y_small_full = np.concatenate(y_small, np.zeros(len(y_large) - len(y_small)))
##ax1.fill_between(x_large, y_large, y_small_full)
#ax1.plot()
#print(x_large)
#print(y_large)
#print(x_small)
#print(y_small)
#print(y_small_full)
#plt.show()

#delta must be < 10


#fig, axes = plt.subplots(figsize = (6,6))
#createCircle(axes, 0,0,0.5)
#axes.set_xlim(-2,2)
#axes.set_ylim(-2,2)
# #plt.show()
