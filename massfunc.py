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
from mpi4py import MPI

rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

def do_snap(ii,z,flist):
    # print "Doing snapshot",ii,"z =",z[ii],flist[ii] 
    logm = rockstar.read_log10mass(flist[ii])
    hist = numpy.histogram(logm,bins=Nbins,range=(M_min,M_max))
    delta = (M_max-M_min)/Nbins
    mf_theory_ps = hmf.MassFunction(dlog10m = delta,z=z[ii],Mmin=M_min,Mmax=M_max,delta_wrt="crit",mf_fit='PS')
    mf_theory_smt = hmf.MassFunction(dlog10m = delta,z=z[ii],Mmin=M_min,Mmax=M_max,delta_wrt="crit",mf_fit='SMT')
    mf_theory_behroozi = hmf.MassFunction(dlog10m = delta,z=z[ii],Mmin=M_min,Mmax=M_max,delta_wrt="crit",mf_fit='Behroozi')
    mf_theory_watson = hmf.MassFunction(dlog10m = delta,z=z[ii],Mmin=M_min,Mmax=M_max,delta_wrt="crit",mf_fit='Watson')
    hist_y = []
    hist_x = []
    for i in range(Nbins):
        hist_x.append(0.5*(hist[1][i]+hist[1][i]))
        hist_y.append(hist[0][i])
    hist_y = (numpy.array(hist_y,dtype=numpy.float64))/112.**3/delta
    plot.rc('text', usetex=True)
    fig = plot.figure()
    ax = fig.add_subplot(111)
    ax.plot(hist_x,hist_y,label="Rockstar")
    ax.plot(mf_theory_ps.,mf_theory_ps.dndlog10m,label="PS")
    ax.plot(mf_theory_smt.M,mf_theory_smt.dndlog10m,label="SMT")
    ax.plot(mf_theory_watson.M,mf_theory_watson.dndlog10m,label="Watson et al. (2012)")
    ax.plot(mf_theory_behroozi.M,mf_theory_behroozi.dndlog10m,label="Behroozi et al. (2012)")
    leg = ax.legend(loc='best', handlelength = 10,ncol=1, fancybox=True, prop={'size':10})
    ax.set_yscale("log")
    ax.text(8.5, 1.e-5, r'$z = '+str(z[ii])+'$')
    ax.set_ylabel(r"$\mathrm{dn/dlog_{10} M (h^3 Mpc^{-3})}$")
    ax.set_xlabel(r"$\mathrm{\log_{10}(M_{200c}/M_\odot)}$")
    fig.savefig("hmf_"+str(z[ii])+".pdf")

def make_runlist(njobs):
    jlist = []
    n = njobs/size
    remain = njobs-n*size
    for i in range(n):
        jlist.append(i*size+rank)
    if rank < remain:
        jlist.append(n*size+rank)
    return jlist

def main(argv):
    z = cubepm.read_zlist()
    flist = cubepm.rockstar_filelist()
    jlist = make_runlist(len(z))
    for i in jlist:
        do_snap(i,z,flist)
        

if __name__ == "__main__":
    main(sys.argv)
        
