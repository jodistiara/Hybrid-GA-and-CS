#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 21:40:00 2019

@author: cdjodistiara
"""

import numpy as np
from math import gamma
from config import Config as cf
from fitness import fitness
import random as rand

# initial population
class Individu:
    def __init__(self):
        self.__allel = np.random.randint(cf.get_maxallel(), \
                                         size=cf.get_dimension())
        self.__fitness = 0
    
    def get_fitness(self):
        return self.__fitness

    def get_allel(self):
        return self.__allel

    def set_fitness(self, value=0):
        if value == 0: self.__fitness = fitness(self.__allel)
        else: self.__fitness = value

    def set_allel(self, array):
        self.__allel = array
    
    def new_egg(self, best, change=True):        # get cuckoo
        new_allel = []
        step_size = np.multiply(best-self.__allel, levy_flight())
        new_allel = (self.__allel + step_size).astype(int)
        new_allel = np.remainder(new_allel, cf.get_maxallel())
        
        new_fitness = fitness(new_allel)
        if change:
            self.__allel = new_allel
            self.__fitness = new_fitness
        else: return new_allel, new_fitness

#*levy flight -- coba cek the coding training, 
def levy_flight(Lambda=cf.get_lambda()):
    #generate step from levy distribution
    size = cf.get_dimension()
    sigma1 = np.power((gamma(1 + Lambda) * np.sin((np.pi * Lambda) / 2)) \
                      / gamma((1 + Lambda) / 2) * Lambda * \
                      np.power(2, (Lambda - 1) / 2), 1 / Lambda)
    sigma2 = 1
    u = np.random.normal(0, sigma1, size=size)
    v = np.random.normal(0, sigma2, size=size)
    step = u / np.power(np.fabs(v), 1 / Lambda)

    return step

def selection(pops):    #----RWS----
    num_of_parents = int(cf.get_Pc()*len(pops))
    fps = []
    selected = []
    total = 0
    for i in range(len(pops)):total += (150000 - pops[i].get_fitness())
    for i in range(len(pops)):
        score = (150000 - pops[i].get_fitness()) / total
        if not fps: fps.append(score)
        else: fps.append(score+fps[i-1])
    for p in range(num_of_parents):
        pointer = rand.random()
        n = 0
        while pointer >= fps[n]: n += 1
        selected.append(pops[n])
    return selected

def crossover(pops):
    offspring = []
    pointer = []
    parent1 = []
    parent2 = []
    
    for k in range(cf.get_kcross()):                    # choose pointer
        r = rand.randint(0, cf.get_dimension()-1)
        while r in pointer:
            r = rand.randint(0, cf.get_dimension()-1)
        pointer.append(r)
    if cf.get_kcross()%2 != 0: pointer.append(cf.get_dimension())
    pointer = sorted(pointer)
    
    if len(pops) >= 2: 
        if len(pops) == 2: n = 1
        else: n = len(pops)
        for i in range(n*2): offspring.append(Individu())
    else: 
        n = 0
        offspring = [pops.copy()]
        
    for i in range(n):
        if i == len(pops)-1:
            parent1 = pops[i].get_allel().copy()
            parent2 = pops[0].get_allel().copy()
        else: 
            parent1 = pops[i].get_allel().copy()
            parent2 = pops[i+1].get_allel().copy()
        
        for j in range(len(pointer)//2):
            temp = parent1[pointer[2*j]:pointer[2*j+1]].copy()
            parent1[pointer[2*j]:pointer[2*j+1]] = parent2[pointer[2*j]:
                                                   pointer[2*j+1]].copy()
            parent2[pointer[2*j]:pointer[2*j+1]] = temp.copy()
        offspring[2*i].set_allel(parent1.copy())
        offspring[2*i].set_fitness()
        offspring[2*i+1].set_allel(parent2.copy())
        offspring[2*i+1].set_fitness()
    return offspring

def mutation(pops):
    numOfGen = len(pops)*cf.get_dimension()
    numOfMutatedGen = int(cf.get_Pm()*numOfGen)
    select = []
    copy_pops = []
    numOfPops = len(pops)
    
    if numOfMutatedGen > 0:
        #copy all offspring's chromosome
        for i in range(numOfPops):
            copy_pops.append(pops[i].get_allel().copy())
        
        for i in range(numOfMutatedGen):
            select = rand.randint(0,(numOfGen-1))   # select gen
            x = select//cf.get_dimension()
            y = select%cf.get_dimension()
            copy_pops[x][y] = rand.randint(0,(cf.get_maxallel()-1))
        
        #set back to original individu object
        for i in range(numOfPops):
            pops[i].set_allel(copy_pops[i].copy())
            pops[i].set_fitness()
    return pops          

def replacement(old, new, algo):
    if algo != 'cs':
        new.extend(old)
    new = sorted(new, reverse=False, key=lambda ID: ID.get_fitness())
    return new[:cf.get_popsize()]

def find_best(pops):
    found = 0
    for i in range(len(pops)):
        if pops[i].get_fitness() <= pops[found].get_fitness(): 
            found = i
    return found

def replace_egg(pops):
    best_egg = find_best(pops)
    
    r = rand.randint(0, len(pops)-1)               # select random egg
    while (r == best_egg):
        r = rand.randint(0, len(pops)-1)
    best = pops[best_egg].get_allel()
    new_egg, value = pops[r].new_egg(best, False)  # create new egg
    
    if value <= pops[r].get_fitness():    # replace if new egg
        pops[r].set_allel(new_egg)        # is better
        pops[r].set_fitness(value)
    return pops

def abandon_egg(pops):
    pops = sorted(pops, reverse=False, key=lambda ID: ID.get_fitness())
    best = pops[0].get_allel()
    for i in range(int(cf.get_Pa() * len(pops))):
        pops[len(pops)-1-i].new_egg(best)
    return pops
