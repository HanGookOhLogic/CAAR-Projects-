import numpy as np 

#Delta
delta = 0.1

#Points

a = (0, np.sqrt(11)/2)

b = (-0.5, 0)
c = (0.5, 0)

d = (  (3 - np.sqrt(33) ) /12    , (np.sqrt((17 - np.sqrt(33))/6))  /2  )
e = (  (-3 + np.sqrt(33) ) /12    , (np.sqrt((17 - np.sqrt(33))/6))  /2  )

f = (  (-3 - np.sqrt(33) )  /12 , (np.sqrt(  (17 + np.sqrt(33))   /6))  /2)
g = (  (3 + np.sqrt(33) )  /12 , (np.sqrt(  (17 + np.sqrt(33))   /6))  /2)


#Edges
edges = [(a,b), (a,d), (a,e), (a,c),
            (b,e), (b,f),
            (c,d), (c,g),
            (d,g),
            (e,f),
            (f,g)]