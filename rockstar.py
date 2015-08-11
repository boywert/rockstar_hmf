import numpy

def read_log10mass(file):
    mass = []
    index = f.readline().split().index("M200c_all")
    print "Looking at column",index
    with open(file,"r") as f
    for line in f:
        if line[0] != "#":
            mass.append(float(line.split()[index]))
    mass = numpy.array(mass)
    return numpy.log10(mass)

