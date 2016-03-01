import numpy
from global_values import *

def read_log10mass(file):
    mass = []
    f = open(file,"r")
    index = f.readline().split().index(column_name)
    f.close()
    print "Looking at column",index
    with open(file,"r") as f:
        for line in f:
            if line[0] != "#":
                mass.append(float(line.split()[index]))
    mass = numpy.array(mass)
    return numpy.log10(mass)

def read_log10mass_all(filelist):
    if len(filelist == 0):
        exit()
    mass = []
    f = open(filelist[0],"r")
    index = f.readline().split().index("M200c_all")
    f.close()
    print "Looking at column",index
    for file in filelist:
        with open(file,"r") as f:
            for line in f:
                line = line.strip()
                if line[0] != "#":
                    mass.append(numpy.log10(float(line.split()[index])))
    mass = numpy.array(mass)
    return mass
