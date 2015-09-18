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


def likelihoodSetup(lnS,mu,nBins,nData):
   #Output: PyMC Model

   # Uniform prior on all variables
   sig    = pymc.Uniform('sig', 0.0, 500.0)
   sig1   = pymc.Uniform('sig1', 0.0, 500.0)
   mu_bar = pymc.Uniform('mu_bar', -5.0, 5.0)
   slope  = pymc.Uniform('slope', -5.0, 5.0)
   norm   = pymc.Uniform('norm', -5.0, 5.0)
 
   #@stochastic(observed=False)
   #mu = [pymc.Normal('mu_s_%i'%i, 0., 1000.0, observed=False)\
   #       for i in range(nBins*nData)]

   @deterministic(plot=False)
   def sBar(slope=slope,norm=norm,mu=mu): return slope * mu + norm

   #@deterministic(plot=False)
   #def stackedM(nBins=nBins,w=w,mu=mu):
   #   mu_s = np.zeros(nBins)
   #   for i in range(nBins): 
   #      mu_s[i] = np.dot( w[i*nData:(i+1)*nData] , mu[i*nData:(i+1)*nData] )
   #   return mu_s

   obs1 = Normal("mu", mu=sBar, tau=sig, value=lnS, observed=True)
   obs2 = Normal("Ms", mu=mu_bar, tau=sig1, value=mu, observed=True)

   return pymc.Model([slope, norm, sig, mu_bar, sig1, obs1, obs2])




