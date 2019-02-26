import numpy as np
import math
from config import Config as cf
import functions as fx
import random as rand

# initial population
class Individu:
    def __init__(self):
        self.__allel = np.random.randint(cf.get_maxgen(), size=cf.get_dimension()) + 1
        self.__fitness = fx.fitness(self.__allel)
    
    def get_fitness(self):
        return self.__fitness

    def get_allel(self):
        return self.__allel

    def set_fitness(self, value):
        self.__fitness = value

    def set_allel(self, array):
        self.__allel = array
    
    #================cuckoo===============
    #get cuckoo
    def new_egg(self):
        new_allel = []
        step_size = cf.get_alpha * levy_flight(cf.get_lambda)
        new_allel = self.__allel + step_size
        new_fitness = fx.fitness(new_allel)

        return new_allel, new_fitness

        #add boundary rules here

    #=================GA====================
    def mutate(self):
        k = cf.get_kmut()
        select = []
        for i in range(k): select.append(rand.randint(0, cf.get_dimension()-1))
        for i in select: 
            self.__allel[i] = rand.randint(1, cf.get_maxallel())
        self.__fitness = fx.fitness(self.__allel)


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

def select_individuals(pops, set_probs):
    selected = []
    num = []
    probs = np.random.uniform(size=len(pops))
    for i, prob in enumerate(probs):
        print(i, ": ", prob)
        if prob < set_probs:
            selected.append(pops[i])
            num.append(i)
    return selected, num

def selection(pops, pointer):
    #----RWS----
    fps = []
    selected = []
    total = 0
    for i in range(len(pops)):total += pops[i].get_fitness()
    for i in range(len(pops)):
        score = pops[i].get_fitness() / total
        if not fps: fps.append(score)
        else: fps.append(score+fps[i-1])
    print("fps: ", fps)
    for p in range(pointer):
        n = rand.random()
        select = 0
        while n > fps[select]:
            select += 1
        # for i, score in enumerate(fps):
        #     if n < score: select = i
        selected.append(pops[select])
        print("n: ", n, " ----> ", select)
        print(selected[p].get_fitness())
    return selected

def crossover(pops):
    offspring = []
    '''
        proses crossover
    '''
    return pops

def mutation(pops, nums):
    for num in nums:
        allel = pops[num].get_allel()
        '''
        proses mutasi
        '''
        pops[num].set_allel(mutated)
        pops[num].set_fitness(fx.fitness(mutated))
    return pops

def replacement(old, new, size=cf.get_popsize()):
    # new_gen = []
    #all = gabung old dan new
    new_gen = sorted(all, reverse=True, key=lambda ID: ID.get_fitness())
    return new_gen[:size]

def abandon_egg(pops):
    for i in range(cf.get_popsize()):
        p = np.random.rand()
        if p < cf.get_Pa():
            pops[i] = new_cuckoo(pops[i])
    return pops
