#!/usr/bin/env python
"""
zip.py

Zero-inflated Poisson example using simulated data.
"""
import numpy as np
from pymc import Uniform, Beta, observed, rpoisson, poisson_like
import numpy.random as npr

# True parameter values
mu_true = 5
sig_true = 0.75
alpha_true = 2.0
n = 100

# Simulate some data
obs1 = np.array([npr.normal(0.0,10.0) for i in range(n)])
obs2 = alpha_true*obs1 + np.array([npr.normal(mu_true,sig_true) for i in range(n)]) 
obs  = np.array([obs1,obs2]).T

# Uniform prior on Poisson mean
mu = Uniform('mu', -20, 20)
# Unifomr prior on psi
sig = Uniform('sig', 0, 5)
# Uniform prior on alpha
alpha = Uniform('alpha', 0, 10)


@observed(dtype=float, plot=False)
def zip(value=obs, alpha=alpha, mu=mu, sig=sig):
 
    # Initialize likeihood
    like = 0.0

    # Loop over data
    for x in value:
       like += - 0.5 * np.log(2.0 * np.pi * sig**2 )\
               - 0.5 * (x[1] - alpha*x[0] - mu)**2/sig**2

    return like

