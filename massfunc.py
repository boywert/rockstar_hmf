import rockstar
import cubepm
import sys
import hmf
import numpy
import matplotlib
matplotlib.use('Agg') 
import pylab as plot
from global_values import *

def do_snap(i,z,flist):
    print "Doing snapshot",i,"z =",z[i],flist[i]
    logm = rockstar.read_log10mass(flist[i])
    hist = numpy.histogram(logm,bins=Nbins,range=(M_min,M_max))
    delta = (M_max-M_min)/Nbins
    mf_theory_behroozi = hmf.MassFunction(dlog10m = delta,z=z[i],Mmin=M_min,Mmax=M_max,delta_wrt="crit",mf_fit='Behroozi')
    mf_theory_watson = hmf.MassFunction(dlog10m = delta,z=z[i],Mmin=M_min,Mmax=M_max,delta_wrt="crit",mf_fit='Watson')
    hist_y = []
    hist_x = []
    for i in range(Nbins):
        hist_x.append(0.5*(hist[1][i]+hist[1][i]))
        hist_y.append(hist[0][i])
    hist_y = (numpy.array(hist_y,dtype=numpy.float64))/112.**3/delta
    print hist_y
    plot.rc('text', usetex=True)
    fig = plot.figure()
    ax = fig.add_subplot(111)
    for i in range(Nbins):
        print hist_x[i],hist_y[i],numpy.log10(mf_theory_watson.M[i]),numpy.log10(mf_theory_behroozi.M[i])
    ax.plot(hist_x,hist_y,label="Rockstar")
    ax.plot(numpy.log10(mf_theory_watson.M),mf_theory_watson.dndlog10m,label="Watson et al. (2012)")
    ax.plot(numpy.log10(mf_theory_behroozi.M),mf_theory_behroozi.dndlog10m,label="Behroozi et al. (2012)")
    leg = ax.legend(loc='best', handlelength = 10,ncol=1, fancybox=True, prop={'size':10})
    fig.savefig("hmf_"+str(z[i])+".pdf")
    
def main(argv):
    z = cubepm.read_zlist()
    flist = cubepm.rockstar_filelist()
    do_snap(int(argv[1]),z,flist)
        

if __name__ == "__main__":
    main(sys.argv)
        
