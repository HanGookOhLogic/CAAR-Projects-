import simulated_annealing
from random import random as rnd
from math import sqrt as sq
from time import clock as cl

from mpi4py import MPI

class Columns(object):
    def __init__(self,r,bg,th,pert=0):
        self.r = r+rnd()*2*pert-pert
        self.bg = bg+rnd()*2*pert-pert
        self.th = th+rnd()*2*pert-pert
        self.p = simulated_annealing.color3kruskal(self.r,self.bg,self.th)
        print(".",end="")
    def merge(c1,c2,p):
        r = (c1.p*c1.r+c2.p*c2.r)/(c1.p+c2.p)
        bg = (c1.p*c1.bg+c2.p*c2.bg)/(c1.p+c2.p)
        th = (c1.p*c1.th+c2.p*c2.th)/(c1.p+c2.p)
        return Columns(r,bg,th,p)
    def rand():
        return Columns(rnd()*0.2+0.5,rnd()*0.2+0.9,rnd()*0.2+0.9)
    def sort(l):
        for i in range(len(l)-1):
            for j in range(len(l)-1):
                if l[j].p>l[j+1].p:
                    t = l[j]
                    l[j] = l[j+1]
                    l[j+1] = t
    def __str__(self):
        return "R:"+str(self.r)+" BG:"+str(self.bg)+" TH:"+str(self.th)+" --> "+str(self.p)

def do():
    size = 20
    numgens = 50
    pertf = lambda x:0.5/sq(x)
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    proc_size = comm.Get_size()
    
    l = [Columns.rand() for i in range(size)]
    #print()
    #[print(n) for n in l]
    #print()
    gen = 1
    gens = []
    t = []
    for n in l:
        t.append(n)
    gens.append(t)
    new_size = size / 2
    while gen<numgens:
        Columns.sort(l)
        [l.pop(-1) for i in range(int(size/2))]
        pert = pertf(gen)
        
        ll = []
        
        num_cols = new_size/proc_size
        for i in range(num_cols*rank, num_cols*(rank+1)):
            ll.append(Columns.merge(l[i],l[(i+1)%new_size],pert))
        
        new_cols = comm.reduce(ll)
        
        if rank == 0:
            l.extend(new_cols)
        
        #print()
        #print("Gen",gen,"done.")
        #[print(n) for n in l]
        #print()
            t = []
            for n in l:
                t.append(n)
            gens.append(t)
        gen+=1
        
def check():
    while True:
        a = rnd()
        b = rnd()
        c = rnd()
        print(a,b,c)
        Columns(a,b,c)

do()
