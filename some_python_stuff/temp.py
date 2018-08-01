from math import cos, acos, pi
from math import sqrt as s
from random import random as r

def b(x):
    if x>s(3)/4:
        return b(s(3)/2-x)
    n = 0
    n += pi - acos(x) - acos(s(3)/2-x)
    n*=2
    if x<1-s(3)/2:
        n += 2*acos(s(3)/2+x)
    return n/2/pi

def f():
    x1 = r()*s(3)/2
    angle = r()*2*pi
    x2 = x1+cos(angle)
    x2 = x2%(s(3)/2)
    return b(x1)*b(x2)

for j in range(10):
    avg = 0
    N = 10000000
    for i in range(N):
        avg+=f()
    print(avg/N)
