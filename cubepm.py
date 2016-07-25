import numpy
from global_values import *
def read_zlist():
    a = open(zlist_file).readlines()
    z = []
    for zi in a:
        z.append(zi.strip())
    return z

def rockstar_filelist():
    flist = []
    z = read_zlist()
    if hasattr(z, "__len__") is False:
        print "xx"
        fname = cat_folder+"/out_0.list"
        flist.append(fname)
    else:
        print "yy"
        for i in range(len(z)):
            fname = cat_folder+"/out_"+str(i)+".list"
            flist.append(fname)
    return flist
