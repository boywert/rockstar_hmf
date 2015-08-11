import numpy

def read_log10mass(file):
    mass = []
    f = open(file,"r")
    index = f.readline().split().index("M200c_all")
    f.seek(0)
    for line in f:
        if line[0] != "#":
            mass.append(float(line.split()[index]))
    f.close()
    mass = numpy.array(mass)
    return numpy.log10(mass)

