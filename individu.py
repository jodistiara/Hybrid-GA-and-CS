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

def selection(pops):
    #----RWS----
    num_of_pointer = cf.get_numofpointer()
    fps = []
    selected = []
    total = 0
    for i in range(len(pops)):total += pops[i].get_fitness()
    for i in range(len(pops)):
        score = pops[i].get_fitness() / total
        if not fps: fps.append(score)
        else: fps.append(score+fps[i-1])
    print("fps: ", fps)
    for p in range(num_of_pointer):
        pointer = rand.random()
        n = 0
        while pointer >= fps[n]:
            n += 1
        # for i, score in enumerate(fps):
        #     if n < score: select = i
        selected.append(pops[n])
        print("pointer: ", ponter, " ----> ", n)
        print(selected[p].get_fitness())
    return selected

def crossover(pops):
    offspring = []
    pointer = []
    parent1 = []
    parent2 = []
    for k in range(cf.get_kcross()):
        r = 1
        while r not in pointer:
            r = rand.randint(0, cf.get_dimension()-1)
        pointer.append(r)
    pointer = sorted(pointer, reverse=False)
    for i in range(int(len(pops)/2)):
        parent1 = pops[(2*i)].get_allel()
        parent2 = pops[(2*i)+1].get_allel()
        for j in range(len(pointer)-1):
            temp = parent1[pointer[2*j]:pointer[2*j+1]].copy()
            parent1[pointer[2*j]:pointer[2*j+1]] = parent2[pointer[j]:pointer[j+1]].copy()
            parent2[pointer[2*j]:pointer[2*j+1]] = temp.copy()
        offspring[(2*i)].set_allel(parent1)
        offspring[(2*i)].set_fitness(fx.fitness(parent1))
        offspring[(2*i)+1].set_allel(parent2)
        offspring[(2*i)+1].set_fitness(fx.fitness(parent2))
    return pops

def replacement(old, new, size=cf.get_popsize()):
    new.extend(old)
    new = sorted(all, reverse=True, key=lambda ID: ID.get_fitness())
    return new[:size]

def abandon_egg(pops):
    for i in range(cf.get_popsize()):
        p = np.random.rand()
        if p < cf.get_Pa():
            allel, fitness = pops[i].new_egg(pops[i])
            pops[i].set_allel(allel)
            pops[i].set_fitness(fitness)
    return pops
