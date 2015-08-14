import numpy
from global_values import *

def read_log10mass(file):
    mass = []
    f = open(file,"r")
    index = f.readline().split().index("M200c_all")
    f.close()
    print "Looking at column",index
    with open(file,"r") as f:
        for line in f:
            if line[0] != "#":
                mass.append(float(line.split()[index])/h0)
    mass = numpy.array(mass)
    return numpy.log10(mass)








