import numpy as np
import math
from config import Config as cf

# initial population
class Chromosome:
    def __init__(self):
        self.__allel = np.random.rand(cf.get_maxgen, size=cf.get_dimension()) + 1
        self.__fitness = fx.fitness(self.__allel)

# crossover

# mutation