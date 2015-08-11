import numpy

def read_log10mass(file):
    mass = []
    f = open(file,"r")
    index = f.readline().split().index("M200c_all")
    print "Looking at column",index
    f.seek(0)
    print "before"
    for line in f:
        if line[0] != "#":
            print line
            mass.append(float(line.split()[index]))
    f.close()
    mass = numpy.array(mass)
    return numpy.log10(mass)

