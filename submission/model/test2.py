import numpy as np
from pymc import Uniform, Beta, observed, Normal,\
                 rpoisson, poisson_like, deterministic, stochastic
import numpy.random as npr
import pymc

import matplotlib.pylab as plt

nor  = 1.0/np.sqrt(2.*np.pi)
nor2 = 1.0/(2.*np.pi)
c    = 299792.46 #light speen (km/s)
zp   = 0.2
lamp = 30.0

def Evolution_factors(zred):
   Ez = np.sqrt(0.23*(1.0+zred)**3 + 0.77)
   #Ez = sqrt(Cosmology.Omega_M*(1.0+zred)**3 + Cosmology.Omega_DE)
   return Ez

#h(z)
def Hubz(zred):
   Ez = Evolution_factors(zred)
   return Ez


def likelihoodSetup(lnS_1,lnS_2,nData):
   #Output: PyMC Model

   # Uniform prior on all variables
   sig1    = pymc.Uniform('sig1', 0.0, 500.0)
   sig2    = pymc.Uniform('sig2', 0.0, 500.0)
   slope1  = pymc.Uniform('slope1', -20.0, 20.0)
   slope2  = pymc.Uniform('slope2', -20.0, 20.0)
   norm1   = pymc.Uniform('norm1', -20.0, 20.0)
   norm2   = pymc.Uniform('norm2', -20.0, 20.0)
 
   #@stochastic(observed=False)
   mu = [pymc.Normal('mu_s_%i'%i, 1., 5.0, observed=False)\
          for i in range(nData)]

   @deterministic(plot=False)
   def sBar1(slope=slope1,norm=norm1,mu=mu): return slope * mu + norm

   @deterministic(plot=False)
   def sBar2(slope=slope2,norm=norm2,mu=mu): return slope * mu + norm

   #@deterministic(plot=False)
   #def stackedM(nBins=nBins,w=w,mu=mu):
   #   mu_s = np.zeros(nBins)
   #   for i in range(nBins): 
   #      mu_s[i] = np.dot( w[i*nData:(i+1)*nData] , mu[i*nData:(i+1)*nData] )
   #   return mu_s

   obs1 = Normal("S_1", mu=sBar, tau=sig, value=lnS, observed=True)
   obs2 = Normal("S_2", mu=mu_bar, tau=sig1, value=mu, observed=True)

   return pymc.Model([slope1, norm1, sig1, slope2, norm2, sig2, obs1, obs2])




