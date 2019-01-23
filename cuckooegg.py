import numpy as np
import math
from config import Config as cf
# import function as fx

#*levy flight -- coba cek the coding training, 
def levy_flight(Lambda):
    #generate step from levy distribution
    size = cf.get_dimension()

    sigma1 = np.power((math.gamma(1 + Lambda) * np.sin((np.pi * Lambda) / 2)) \
                      / math.gamma((1 + Lambda) / 2) * np.power(2, (Lambda - 1) / 2), 1 / Lambda)
    sigma2 = 1
    u = np.random.normal(0, sigma1, size=size)
    v = np.random.normal(0, sigma2, size=size)
    step = u / np.power(np.fabs(v), 1 / Lambda)

    return step

#abandon nest <-- abandon allel and replace with new 1, or egg??
def abandon_variable(egg):
    # abandon some variables
    for i in range(len(egg)):
        p = np.random.rand()
        if p < cf.get_Pa():
            egg[i] = np.random.randint(cf.get_maxallel() + 1)
    return egg

def abandon_egg(pops):
    for i in range(cf.get_popsize()):
        p = np.random.rand()
        if p < cf.get_Pa():
            pops[i] = new_cuckoo(pops[i])
    return pops

#get cuckoo
def new_egg(egg):
    step_size = cf.get_alpha * levy_flight(cf.get_lambda)
    egg = egg + step_size
    return egg




