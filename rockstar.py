import numpy

def read_log10mass(file):
    mass = []
    f = open(file,"r")
    index = f.readline().split().index("M200c_all")
    print "Looking at column",index
    f.seek(0)
    for line in f:
        print line
        if line[0] != "#":
            mass.append(float(line.split()[index]))
    f.close()
    mass = numpy.array(mass)
    return numpy.log10(mass)

