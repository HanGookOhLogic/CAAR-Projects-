import numpy as np

#Delta
delta = 0.01

#Points
c = (0,0) #center

a = (0,1) #outer nodes
b = (np.sqrt(3)/2, 0.5)
d = (np.sqrt(3)/2, -0.5)
f = (0, -1)
g = (-(np.sqrt(3)/2), -0.5)
h = (-(np.sqrt(3)/2), 0.5)

r = (-0.552815, 0.1653)
t = (0.420395, 0.395217)
s = (0.130887, -0.561959)

points = [c, a, b, d, f, g, h, r, s, t]

#Edges
edges = [(a,b),(a,c),(a,h),(a,r),
        (b,d),(b,c),
        (d,t),(d,c),(d,f),
        (f,c), (f,g),
        (g,s), (g,c), (g,h),
        (h,c),
        (r,t),
        (t,s),
        (s,r)]


