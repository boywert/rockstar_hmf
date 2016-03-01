import numpy
from global_values import *
def read_zlist():
    z = numpy.loadtxt(zlist_file)
    return z

def rockstar_filelist():
    flist = []
    z = read_zlist()
    print z
    if numpy.isscalar(z):
        print "xx"
        fname = cat_folder+"/out_0.list"
        flist.append(fname)
    else:
        print "yy"
        for i in range(len(z)):
            fname = cat_folder+"/out_"+str(i)+".list"
            flist.append(fname)
    return flist
