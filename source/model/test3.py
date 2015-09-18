import numpy as np
from pymc import Uniform, Beta, observed, Normal,\
                rpoisson, poisson_like, deterministic, stochastic, potential
import pymc
import numpy.random as npr; import pymc
import matplotlib.pylab as plt
from generateData2 import generateDataMCMC
from selectionFunction import selectionFunction
from inputParameters import * #beta1, beta2

nor  = 1.0/np.sqrt(2.*np.pi); nor2 = 1.0/(2.*np.pi)
c = 299792.46 #light speen (km/s)

def likelihoodSetup(xObs,yObs,xObsErr,yObsErr):
   #Output: PyMC Model
   # Uniform prior on all variables
   n = len(xObs) #float(len(xObs))
   lnLxCut = -0.5;   lnLxCut2 = 1.5
   beta1x= beta1;   beta2x= beta2

   sigYX = pymc.Uniform('sigYX', 0.05,2.0)
   slopeYX = pymc.Uniform('slopeYX', -5.0, 5.0)
   normYX = pymc.Uniform('normYX', -5.0, 5.0)
   x = [pymc.Normal('x_%i'%i, mu=beta1/beta2, tau=beta2, observed=False)\
          for i in range(n)]
   #Y = [pymc.Normal('y_%i'%i, mu=yObs, tau=1./yObsErr**2, observed=False)\
   #       for i in range(n)]

   @deterministic(plot=False)
   def yBar(slope=slopeYX,norm=normYX,x=x): return slope*x + norm

   @deterministic(plot=False)
   def selectionL(): return lnLxCut

   @deterministic(plot=False)
   def selectionU(): return lnLxCut2

   @deterministic(plot=False)
   def tauY(sig=sigYX,sigO=yObsErr): return 1.0/(sig**2 + sigO**2)  
  
   @deterministic(plot=False)
   def tauX(sigO=xObsErr): return 1.0/sigO**2
 
   obs1 = Normal("X", mu=x, tau=tauX, value=xObs, observed=True)
   obs2 = pymc.TruncatedNormal("Y", mu=yBar, tau=tauY,\
                      a=selectionL, b=selectionU,\
                      value=yObs, observed=True)

   return pymc.Model([normYX, slopeYX, sigYX, obs1, obs2])


def likelihoodSetup2(xObs,yObs,xObsErr,yObsErr):
   #Output: PyMC Model
   # Uniform prior on all variables
   n = float(len(xObs))
   sigYX = pymc.Uniform('sigYX', 0.05,2.0)
   slopeYX = pymc.Uniform('slopeYX', -5.0, 5.0)
   normYX = pymc.Uniform('normYX', -5.0, 5.0)
   beta1x= beta1 #pymc.Uniform('beta1', -10.0, 10.0)
   beta2x= beta2 #pymc.Uniform('beta2', 0.0, 10.0)

   @deterministic(plot=False)
   def yBar(slope=slopeYX,norm=normYX,x=xObs): return slope*x + norm

   obs1 = Normal("X", mu=beta1/beta2, tau=beta2, value=xObs, observed=True)
   obs2 = Normal("Y", mu=yBar, tau=1./sigYX**2,  value=yObs, observed=True)

   return pymc.Model([normYX, slopeYX, sigYX, obs1, obs2])



def likelihoodSetupOld(xObs,yObs,xObsErr,yObsErr):
   #Output: PyMC Model
   # Uniform prior on all variables
   n = len(xObs) #float(len(xObs))
   sigYX = pymc.Uniform('sigYX', 0.05,2.0)
   slopeYX = pymc.Uniform('slopeYX', -5.0, 5.0)
   normYX = pymc.Uniform('normYX', -5.0, 5.0)
   N = 1050 #pymc.DiscreteUniform('N', n, 30.0*n)
   lnLxCut = -0.5
   lnLxCut2 = 1.5
   beta1x= beta1 #pymc.Uniform('beta1', -10.0, 10.0)
   beta2x= beta2 #pymc.Uniform('beta2', 0.0, 10.0)

   @deterministic(plot=False)
   def yBar(slope=slopeYX,norm=normYX,x=xObs): return slope*x + norm

   @deterministic(plot=False)
   def probI(sigYX=sigYX, slopeYX=slopeYX, normYX=normYX,yBar=yBar, N=N):
      _,ym = generateDataMCMC(normYX, slopeYX, sigYX, ndata=2000000)
      mask = selectionFunction(ym) 
      print sigYX, slopeYX, normYX, N, float(sum(mask))/float(len(mask))
      return float(sum(mask))/float(len(mask))

   @deterministic(plot=False)
   def selectionL(): return lnLxCut

   @deterministic(plot=False)
   def selectionU(): return lnLxCut2
      
   obs1 = Normal("X", mu=beta1/beta2, tau=beta2, value=xObs, observed=True)
   #obs2 = Normal("Y", mu=yBar, tau=1./sigYX**2,  value=yObs, observed=True)
   #obs3 = pymc.Binomial("n", n=N, p=probI, value=n, observed=True)

   obs2 = pymc.TruncatedNormal("Y", mu=yBar, tau=1./sigYX**2,\
                      a=selectionL, b=selectionU,\
                      value=yObs, observed=True)

   """
   @observed(dtype=float, plot=False)
   def selection(value=n, sigYX=sigYX, slopeYX=slopeYX, normYX=normYX,\
                 yBar=yBar, N=N):
      _,ym = generateDataMCMC(normYX, slopeYX, sigYX, ndata=500)
      mask = selectionFunction(ym) 
      probI = float(sum(mask))/float(len(mask))
      #C_Nn = N*np.log(N) - n*np.log(n) - (N-n)*np.log(N-n) 
      loglike = pymc.binomial_like(n,N,probI)
      #(N-n)*np.log(1.0-probI) + n*np.log(probI)
      #loglike2 = pymc.normal_like(xObs,mu=beta1/beta2,tau=beta2)
      #loglike3 = pymc.normal_like(yObs,mu=yBar,tau=1./sigYX**2)
      #loglike = -n*np.log(probI+0.0001)
   """
   return "NOTHING"

