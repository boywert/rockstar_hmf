#!/home1/01937/cs390/massfunction/boyd/bin/python
import rockstar
import cubepm
import sys
import hmf
import numpy
import matplotlib
matplotlib.use('Agg')
import pylab as plot
from global_values import *


# from mpi4py import MPI
# rank = MPI.COMM_WORLD.Get_rank()
# size = MPI.COMM_WORLD.Get_size()

def do_snap(ii,zstring,flist,single = 1):
    z = numpy.zeros(len(zstring))
    for iii in range(len(zstring)):
        z[iii] = float(zstring[iii])
    print "Doing snapshot",ii,"z =",zstring[ii]
    hist = numpy.histogram([],bins=Nbins,range=(M_min,M_max))
    t_hist = hist[0]
    if single:
        logm = rockstar.read_log10mass(flist[ii])
        t_hist = numpy.histogram(logm,bins=Nbins,range=(M_min,M_max))[0]
    else:
        flist = [cat_folder+"/zhalo_"+zstring[ii]+"/halos_"+zstring[ii]+"."+str(i)+".ascii" for i in range(filespersnap) ]
        for flistii in flist:
            print "Doing file: ",flistii
            logm = rockstar.read_log10mass(flistii)
            t_hist += numpy.histogram(logm,bins=Nbins,range=(M_min,M_max))[0]
    delta = (M_max-M_min)/Nbins
    mf_theory_ps = hmf.MassFunction(dlog10m = delta,z=z[ii],Mmin=M_min,Mmax=M_max,delta_wrt="crit",hmf_model='PS')
    mf_theory_smt = hmf.MassFunction(dlog10m = delta,z=z[ii],Mmin=M_min,Mmax=M_max,delta_wrt="crit",hmf_model='SMT')
    mf_theory_behroozi = hmf.MassFunction(dlog10m = delta,z=z[ii],Mmin=M_min,Mmax=M_max,delta_wrt="crit",hmf_model='Behroozi')
    mf_theory_watson = hmf.MassFunction(dlog10m = delta,z=z[ii],Mmin=M_min,Mmax=M_max,delta_wrt="crit",hmf_model='Watson')
    hist_y = []
    hist_x = []
    for i in range(Nbins):
        hist_x.append(hist[1][i])
        hist_y.append(t_hist[i])
    hist_y = (numpy.array(hist_y,dtype=numpy.float64))/boxsize**3/delta
    print hist_x,hist_y
    plot.rc('text', usetex=True)
    fig = plot.figure()
    ax = fig.add_subplot(111)
    ax.plot(hist_x,hist_y,label="Rockstar")
    ax.plot(numpy.log10(mf_theory_ps.M),mf_theory_ps.dndlog10m,label="PS")
    ax.plot(numpy.log10(mf_theory_smt.M),mf_theory_smt.dndlog10m,label="SMT")
    ax.plot(numpy.log10(mf_theory_watson.M),mf_theory_watson.dndlog10m,label="Watson et al. (2012)")
    ax.plot(numpy.log10(mf_theory_behroozi.M),mf_theory_behroozi.dndlog10m,label="Behroozi et al. (2012)")
    leg = ax.legend(loc='best', handlelength = 10,ncol=1, fancybox=True, prop={'size':10})
    ax.set_yscale("log")
    ax.text(8.5, 1.e-5, r'$z = '+str(z[ii])+'$')
    ax.set_ylabel(r"$\mathrm{dn/dlog_{10} M (h^3 Mpc^{-3})}$")
    ax.set_xlabel(r"$\mathrm{\log_{10}( h M_{200c}/M_\odot)}$")
    fig.savefig("hmf_"+zstring[ii]+".pdf")

# def make_runlist(njobs):
#     jlist = []
#     n = njobs/size
#     remain = njobs-n*size
#     for i in range(n):
#         jlist.append(i*size+rank)
#     if rank < remain:
#         jlist.append(n*size+rank)
#     return jlist

from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
def main(argv):
    z = cubepm.read_zlist()
    flist = cubepm.rockstar_filelist()
    # jlist = make_runlist(len(z))
    # for i in jlist:
    zindex = numpy.arange(len(z))
    #numpy.random.shuffle(zindex)
    zindex_node = numpy.array_split(zindex,size)
    #for i in zindex_node[rank]:
    do_snap(40,z,flist,1)


if __name__ == "__main__":
    main(sys.argv)
