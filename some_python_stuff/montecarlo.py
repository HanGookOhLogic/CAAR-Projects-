from math import *
from random import random as r

##############################################
#                MAIN TOOLS                  #
#--------------------------------------------#
#  LINE CLASS: REPRESENTS A LINEAR BOUND ON  #
#              X AND Y                       #
#                                            #
#   SET CLASS: REPRESENTS A GROUP OF LINEAR  #
#              BOUNDS ON X AND Y (A GROUP    #
#              OF LINES)                     #
#                                            #
#VECTOR CLASS: REPRESENTS A VECTOR (HELPS    #
#              WITH IMPLEMENTATION OF        #
#              PARALLELOGRAM CLASS)          #
#                                            #
#PAR... CLASS: REPRESENTS A PARALLELOGRAM    #
#              FOR THE SPECIFIC PURPOSE OF   #
#              USING A PARALLELOGRAM AS A    #
#              TILEBLOCK                     #
#                                            #
# TEST METHOD: RUNS MONTE CARLO SIMULATION   #
#              GIVEN THE LENGTH/WIDTH OF     #
#              A RECTANGLE (FOR WRAPPING),   #
#              A NUMBER OF REPETITIONS, AND  #
#              A DICTIONARY MAPPING REGIONS  #
#              (WHICH ARE SETS) TO COLORS.   #
#              WITH EACH REPETITION, WE      #
#              CHOOSE A RANDOM POINT IN THE  #
#              REGION AND THEN CHOOSE A      #
#              RANDOM POINT ONE UNIT AWAY    #
#              FROM THE FIRST ONE, COMPARE   #
#              THEIR COLORS, AND ADD ONE TO  #
#              A "BADNESS" COUNT IF THEY'RE  #
#              THE SAME. WE THEN CALCULATE   #
#              THE FRACTION OF PAIRS THAT    #
#              WERE BAD                      #
#                                            #
#TESTP METHOD: RUNS MONTE CARLO SIMULATION   #
#              GIVEN A PARALLELOGRAM TILE-   #
#              BLOCK, A NUMBER OF REPS, AND  #
#              A DICTIONARY MAPPING REGIONS  #
#              (WHICH ARE SETS) TO COLORS    #
##############################################

class Line(object):
    def __init__(self,a,b,c,less):
        """ax+by < or > c"""
        self.a = a
        self.b = b
        self.c = c
        self.less = less
    def sat(self,x,y):
        """check if the point (x,y) satisfies the inequality"""
        if self.less:
            return self.a*x+self.b*y < self.c
        return self.a*x+self.b*y > self.c
    def __str__(self):
        if self.less:
            return str(self.a)+"x+"+str(self.b)+"y < "+str(self.c)
        return str(self.a)+"x+"+str(self.b)+"y > "+str(self.c)

class Set(object):
    def __init__(self,*args):
        """takes a set of lines"""
        self.lines = args
    def sat(self,x,y):
        for line in self.lines:
            if not line.sat(x,y):
                return False
        return True
    def __str__(self):
        s = ""
        for line in self.lines:
            s+=str(line)+"\n"
        return s

class Vector(object):
    def __init__(self,x,y):
        self.xy = [x,y]
        self.x = x
        self.y = y
    def __add__(self,other):
        return Vector(self.x+other.x,self.y+other.y)
    def __sub__(self,other):
        return Vector(self.x-other.x,self.y-other.y)
    def gen(x1,x2,y1,y2):
        return Vector(r()*(x2-x1)+x1,r()*(y2-y1)+y1)
    def __mul__(self,scalar):
        return Vector(self.x*scalar,self.y*scalar)

class Parallelogram(object):
    def __init__(self,v1,v2):
        #make sure v1 is the bottom side of the parallelogram
        self.v1 = v1
        self.v2 = v2
        self.diag = v1+v2
        bl = [-self.diag.x/2,-self.diag.y/2]
        tr = [self.diag.x/2,self.diag.y/2]
        self.l1 = Line(v1.y,-v1.x,v1.y*bl[0]-v1.x*bl[1],False)
        self.l2 = Line(v2.y,-v2.x,v2.y*bl[0]-v2.x*bl[1],False)
        self.l3 = Line(v1.y,-v1.x,v1.y*tr[0]-v1.x*tr[1],True)
        self.l4 = Line(v2.y,-v2.x,v2.y*tr[0]-v2.x*tr[1],True)
        self.s = Set(self.l1,self.l2,self.l3,self.l4)
        print(self.l1,self.l2,self.l3,self.l4)
    def mod(self,x,y):
        while not self.l1.sat(x,y):
            x += self.v2.x
            y += self.v2.y
        while not self.l2.sat(x,y):
            x += self.v1.x
            y += self.v1.y
        while not self.l3.sat(x,y):
            x -= self.v2.x
            y -= self.v2.y
        while not self.l4.sat(x,y):
            x -= self.v1.x
            y -= self.v1.y
        return x, y
    def gen(self):
        x1, y1 = r()*self.diag.x-self.diag.x/2, r()*self.diag.y-self.diag.y/2
        while not self.s.sat(x1,y1):
            x1, y1 = r()*self.diag.x-self.diag.x/2, r()*self.diag.y-self.diag.y/2
        theta = r()*2*pi
        x2, y2 = self.mod(x1+cos(theta)), self.mod(y1+sin(theta))
        return x1, y1, x2, y2

def test(x,y,reps,dyct):
    #bad count
    bad = 0
    for rep in range(reps):
        #first pair of points
        x1 = r()*x
        y1 = r()*y
        #choose a random angle/direction to move
        theta = r()*2*pi
        #second point one unit away
        x2 = (x1+cos(theta))%x-x/2
        y2 = (y1+sin(theta))%y-y/2
        #fix to be centered at 0
        x1-=x/2
        y1-=y/2
        #check which region contains the first point
        for s in dyct:
            if s.sat(x1,y1):
                c1 = dyct[s]
                break
        #check which region contains the second point
        for s in dyct:
            if s.sat(x2,y2):
                c2 = dyct[s]
                break
        #if the colors are the same, increase the count
        #print(c1,c2)
        if c1 == c2:
            bad +=1
    return float(bad)/reps, bad

def testp(v1, v2, reps, dyct):
    p = Parallelogram(v1, v2)
    bad = 0
    for rep in range(reps):
        print("genning points")
        x1, y1, x2, y2 = p.gen()
        print("points genned")
        for s in dyct:
            if s.sat(x1,y1):
                c1 = dyct[s]
                break
        for s in dyct:
            if s.sat(x2,y2):
                c2 = dyct[s]
                break
        print(c1,c2)
        if c1 == c2:
            bad += 1
    return bad/reps



###############################
#           REGIONS           #
#-----------------------------#
#  HEXAGON: REPRESENTS A      #
#           HEXAGON CENTERED  #
#           AT (X,Y) WITH     #
#           DIAMETER D        #
# PEGGPENT: REPRESENTS A      #
#           PENTAGON DERIVED  #
#           FROM THE HEPTAGON #
#           OF ED PEGG JR.'S  #
#           7-COLORING OF THE #
#           PLANE             #
###############################
class Hexagon(object):
    """Represents a hexgon centered at the point (x,y) with diameter d"""
    def __init__(self,x,y,d):
        #six sides
        l1 = Line(0,1,y-d*sqrt(3)/4,False)
        l2 = Line(0,1,y+d*sqrt(3)/4,True)
        l3 = Line(-sqrt(3),1,y-sqrt(3)*(x+d/2),False)
        l4 = Line(-sqrt(3),1,y-sqrt(3)*(x-d/2),True)
        l5 = Line(sqrt(3),1,y+sqrt(3)*(x+d/2),True)
        l6 = Line(sqrt(3),1,y+sqrt(3)*(x-d/2),False)
        self.s = Set(l1,l2,l3,l4,l5,l6)
    def sat(self,x,y):
        return self.s.sat(x,y)
    def H(v,d):
        return Hexagon(v.x,v.y,d)

class Triangle(object):
    def __init__(self,x,y,d,up):
        b = {True:1,False:-1}[up]
        l1 = Line(0,1,y,not up)
        l2 = Line(sqrt(3),1,sqrt(3)*(x+b*d/2)+y,up)
        l3 = Line(-sqrt(3),1,-sqrt(3)*(x-b*d/2)+y,up)
        self.s = Set(l1,l2,l3)
    def sat(self,x,y):
        return self.s.sat(x,y)
    def T(v,d,up):
        return Triangle(v.x,v.y,d,up)

class Square(object):
    def __init__(self,x,y,d):
        self.x = x
        self.y = y
        self.d = d
        l1 = Line(0,1,y+d/2,True)
        l2 = Line(0,1,y-d/2,False)
        l3 = Line(1,0,x+d/2,True)
        l4 = Line(1,0,x-d/2,False)
        self.s = Set(l1,l2,l3,l4)
    def sat(self,x,y):
        return self.s.sat(x,y)
    def __str__(self):
        return str(self.s)

class PeggPent(object):
    def __init__(self,x,y,up):
        b = {True:1,False:-1}[up]
        d = (1+sqrt(7))/4
        l1 = Line(0,1,y,not up)
        l2 = Line(1,0,x-d/2,False)
        l3 = Line(1,0,x+d/2,True)
        l4 = Line(1,b,x+b*y+d,True)
        l5 = Line(1,-b,x-b*y-d,False)
        self.s = Set(l1,l2,l3,l4,l5)
    def sat(self,x,y):
        return self.s.sat(x,y)
    def __str__(self):
        return str(self.s)

class PritPent(object):
    def __init__(self,x,y,right):
        s = {True:1.0,False:-1.0}[right]
        m = 2.49557
        b = 0.013622
        m21 = sqrt(m**2+1)
        l1 = Line(1,0,x,not right)
        l2 = Line(0,1,y-0.25,False)
        l3 = Line(0,1,y+0.25,True)
        l4 = Line(-m,1,-m*x-s*m21+s*0.25+s*b+y,not right)
        l5 = Line(m,1,m*x+s*m21-s*0.25-s*b+y,right)
        self.s = Set(l1,l2,l3,l4,l5)
    def sat(self,x,y):
        return self.s.sat(x,y)

###############################
#            TESTING          #
#-----------------------------#
#TESTHEX3: HEXAGON 3-COLORING #
#TESTHEX4: HEXAGON 4-COLORING #
#TESTPEGG6: ~PEGG 6-COLORING  #
###############################

def testHex3(d):
    r1 = Hexagon(0,0,d)
    r2 = Hexagon(3*d/4,3*sqrt(3)*d/4,d)
    r3 = Hexagon(3*d/4,-3*sqrt(3)*d/4,d)
    r4 = Hexagon(-3*d/4,3*sqrt(3)*d/4,d)
    r5 = Hexagon(-3*d/4,-3*sqrt(3)*d/4,d)
    b1 = Hexagon(0,d*sqrt(3)/2,d)
    b2 = Hexagon(-3*d/4,-d*sqrt(3)/4,d)
    b3 = Hexagon(3*d/4,-d*sqrt(3)/4,d)
    g1 = Hexagon(0,-d*sqrt(3)/2,d)
    g2 = Hexagon(-3*d/4,d*sqrt(3)/4,d)
    g3 = Hexagon(3*d/4,d*sqrt(3)/4,d)
    dyct = {r1:0,r2:0,r3:0,r4:0,r5:0,b1:1,b2:1,b3:1,g1:2,g2:2,g3:2}
    return test(3*d/2,3*sqrt(3)/2*d,10000,dyct)

def testBar3(r,bg,th):
    x1 = Line(1,0,-r-bg,False)
    x2 = Line(1,0,-bg,True)
    x3 = Line(1,0,-bg,False)
    x4 = Line(1,0,0,True)
    x5 = Line(1,0,0,False)
    x6 = Line(1,0,r,True)
    x7 = Line(1,0,r,False)
    x8 = Line(1,0,r+bg,True)
    y1 = Line(0,1,-th,False)
    y2 = Line(0,1,0,True)
    y3 = Line(0,1,0,False)
    y4 = Line(0,1,th,True)
    r1 = Set(x1,x2)
    r2 = Set(x5,x6)
    b1 = Set(x3,x4,y1,y2)
    b2 = Set(x7,x8,y3,y4)
    g1 = Set(x3,x4,y3,y4)
    g2 = Set(x7,x8,y1,y2)
    dyct = {r1:0,r2:0,b1:1,b2:1,g1:2,g2:2}
    return test(2*(r+bg),2*th,10000,dyct)

def testHex4(d):
    r1 = Hexagon(0,0,d)
    r2 = Hexagon(-3*d/2,d*sqrt(3)/2,d)
    r3 = Hexagon(-3*d/2,-d*sqrt(3)/2,d)
    r4 = Hexagon(3*d/2,d*sqrt(3)/2,d)
    r5 = Hexagon(3*d/2,-d*sqrt(3)/2,d)
    b1 = Hexagon(-3*d/2,0,d)
    b2 = Hexagon(3*d/2,0,d)
    b3 = Hexagon(0,d*sqrt(3)/2,d)
    b4 = Hexagon(0,-d*sqrt(3)/2,d)
    g1 = Hexagon(-d*3/4,d*sqrt(3)/4,d)
    g2 = Hexagon(d*3/4,-d*sqrt(3)/4,d)
    y1 = Hexagon(d*3/4,d*sqrt(3)/4,d)
    y2 = Hexagon(-d*3/4,-d*sqrt(3)/4,d)
    dyct = {r1:0,r2:0,r3:0,r4:0,r5:0,b1:1,b2:1,b3:1,b4:1,g1:2,g2:2,y1:3,y2:3}
    return test(3*d,sqrt(3)*d,100000,dyct)

def testBar4(w,th):
    r = w
    bg = w
    x1 = Line(1,0,-r-bg,False)
    x2 = Line(1,0,-bg,True)
    x3 = Line(1,0,-bg,False)
    x4 = Line(1,0,0,True)
    x5 = Line(1,0,0,False)
    x6 = Line(1,0,r,True)
    x7 = Line(1,0,r,False)
    x8 = Line(1,0,r+bg,True)
    y1 = Line(0,1,-th,False)
    y2 = Line(0,1,0,True)
    y3 = Line(0,1,0,False)
    y4 = Line(0,1,th,True)
    r1 = Set(x1,x2,y3,y4)
    r2 = Set(x5,x6,y1,y2)
    b1 = Set(x3,x4,y3,y4)
    b2 = Set(x7,x8,y1,y2)
    g1 = Set(x5,x6,y3,y4)
    g2 = Set(x1,x2,y1,y2)
    ye1 = Set(x7,x8,y3,y4)
    ye2 = Set(x3,x4,y1,y2)
    dyct = {r1:0,r2:0,b1:1,b2:1,g1:2,g2:2,ye1:3,ye2:3}
    return test(2*(r+bg),2*th,10000,dyct)

def testSq5(d):
    g = lambda x,y:Square((x-3)*d,(y-3)*d,d)
    b = [g(1,1),g(2,4),g(3,2),g(4,5),g(5,3)]
    o = [g(1,2),g(2,5),g(3,3),g(4,1),g(5,4)]
    e = [g(1,3),g(2,1),g(3,4),g(4,2),g(5,5)]
    y = [g(1,4),g(2,2),g(3,5),g(4,3),g(5,1)]
    r = [g(1,5),g(2,3),g(3,1),g(4,4),g(5,2)]
    #[[print(s) for s in l] for l in [b,o,e,y,r]]
    dyct = {}
    for i in range(5):
        dyct[b[i]] = 0
        dyct[o[i]] = 1
        dyct[e[i]] = 2
        dyct[y[i]] = 3
        dyct[r[i]] = 4
    return test(5*d,5*d,10000,dyct)

def testHexTri5(dh,dt):
    ul = Vector(-1/2,sqrt(3)/2)
    ur = Vector(1/2,sqrt(3)/2)
    r = Vector(1,0)
    dr = Vector(1/2,-sqrt(3)/2)
    dl = Vector(-1/2,-sqrt(3)/2)
    l = Vector(-1,0)
    pv1 = ((ur+r)*(dh/2)+dr*dt)*2
    pv2 = ((ul+ur)*(dh/2)+r*dt)*2
    hr = (r+ur)*(dh/2)+dr*dt
    hu = (ul+ur)*(dh/2)+r*dt
    htv = r*(dt/2)
    ghex = Hexagon(0,0,dh)
    yhex1 = Hexagon.H(hr+hu,dh)
    yhex2 = Hexagon.H((hr+hu)*(-1),dh)
    yhex3 = Hexagon.H(hu-hr,dh)
    yhex4 = Hexagon.H(hr-hu,dh)
    rhex1 = Hexagon.H(hr,dh)
    rhex2 = Hexagon.H(hr*-1,dh)
    bhex1 = Hexagon.H(hu,dh)
    bhex2 = Hexagon.H(hu*-1,dh)
    ptri1 = Triangle.T(hr*(-1)+dr*(dh/2)-htv,dt,False)
    ptri2 = Triangle.T(dl*(dh/2)-htv,dt,True)
    ptri3 = Triangle.T(dr*(dh/2)-htv,dt,False)
    ptri4 = Triangle.T(hu-hr+dr*(dh/2)-htv,dt,False)
    ptri5 = Triangle.T(hr-hu+ul*(dh/2)+htv,dt,True)
    ptri6 = Triangle.T(ul*(dh/2)+htv,dt,True)
    ptri7 = Triangle.T(ur*(dh/2)+htv,dt,False)
    ptri8 = Triangle.T(hr+ul*(dh/2)+htv,dt,True)
    dyct = {ghex:0,yhex1:1,yhex2:1,yhex3:1,yhex4:1,rhex1:2,rhex2:2,bhex1:3,bhex2:3,ptri1:4,ptri2:4,ptri3:4,ptri4:4,ptri5:4,ptri6:4,ptri7:4,ptri8:4}
    return testp(pv1,pv2,10000,dyct)

def testPegg6():
    d = (1+sqrt(7))/4
    r1 = PeggPent(-d,d*1.5,False)
    r2 = PeggPent(d/2,0,False)
    b1 = PeggPent(0,d*1.5,False)
    b2 = PeggPent(-d*1.5,0,False)
    b3 = PeggPent(d*1.5,0,False)
    g1 = PeggPent(d,d*1.5,False)
    g2 = PeggPent(-d/2,0,False)
    t1 = PeggPent(-d*1.5,0,True)
    t2 = PeggPent(0,-d*1.5,True)
    t3 = PeggPent(d*1.5,0,True)
    y1 = PeggPent(-d,-d*1.5,True)
    y2 = PeggPent(d/2,0,True)
    p1 = PeggPent(-d/2,0,True)
    p2 = PeggPent(d,-d*1.5,True)
    dyct = {r1:0,r2:0,b1:1,b2:1,b3:1,g1:2,g2:2,t1:3,t2:3,t3:3,y1:4,y2:4,p1:5,p2:5}
    return test(3*d,3*d,100000,dyct)

def testPrit6():
    m = 2.49557
    b = 0.013622
    m21 = sqrt(m**2+1)
    c = (2*m21-0.75-2*b)/m
    r1 = PritPent(c,0.5,False)
    r2 = PritPent(0,-0.25,False)
    b1 = PritPent(c,0,False)
    b2 = PritPent(0,0.75,False)
    b3 = PritPent(0,-0.75,False)
    g1 = PritPent(c,-0.5,False)
    g2 = PritPent(0,0.25,False)
    y1 = PritPent(-c,0.5,True)
    y2 = PritPent(0,-0.25,True)
    t1 = PritPent(-c,0,True)
    t2 = PritPent(0,-0.75,True)
    t3 = PritPent(0,0.75,True)
    p1 = PritPent(-c,-0.5,True)
    p2 = PritPent(0,0.25,True)
    dyct = {r1:0,r2:0,b1:1,b2:1,b3:1,g1:2,g2:2,y1:3,y2:3,t1:4,t2:4,t3:4,p1:5,p2:5}
