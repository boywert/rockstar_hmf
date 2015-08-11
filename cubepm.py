import numpy
from global_values import *
def read_zlist():
    z = numpy.loadtxt(zlist_file)
    return z

def rockstar_filelist():
    flist = []
    z = read_zlist()
    for i in range(len(z)):
        fname = cat_folder+"/out_"+str(i)+".list"
        flist.append(fname)
    return flist
