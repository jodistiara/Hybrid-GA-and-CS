#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 21:40:00 2019

@author: cdjodistiara
"""

import numpy as np
import math
from config import Config as cf
from fitness import fitness
import random as rand

# initial population
class Individu:
    def __init__(self):
        self.__allel = np.random.randint(cf.get_maxallel(), size=cf.get_dimension())
        self.__fitness = 0
    
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
        step_size = cf.get_alpha() * levy_flight(cf.get_lambda())
        new_allel = (self.__allel + step_size).astype(int)
    
        #boundary rules
        for i, allel in enumerate(new_allel):
            if allel >= cf.get_maxallel():
                new_allel[i] = allel % cf.get_maxallel()
        
        new_fitness = fitness(new_allel)

        return new_allel, new_fitness

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

def selection(pops):    #----RWS----
    num_of_pointer = int(cf.get_Pc()*len(pops))
    fps = []
    selected = []
    total = 0
    for i in range(len(pops)):total += pops[i].get_fitness()
    for i in range(len(pops)):
        score = pops[i].get_fitness() / total
        if not fps: fps.append(score)
        else: fps.append(score+fps[i-1])
    for p in range(num_of_pointer):
        pointer = rand.random()
        n = 0
        while pointer >= fps[n]:
            n += 1
        selected.append(pops[n])
    return selected

def crossover(pops):
    offspring = []
    pointer = []
    parent1 = []
    parent2 = []
    
    for k in range(cf.get_kcross()):
        r = rand.randint(0, cf.get_dimension()-1)
        while r in pointer:
            r = rand.randint(0, cf.get_dimension()-1)
        pointer.append(r)
    pointer = sorted(pointer, reverse=False)
    
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
            parent1[pointer[2*j]:pointer[2*j+1]] = parent2[pointer[2*j]:pointer[2*j+1]].copy()
            parent2[pointer[2*j]:pointer[2*j+1]] = temp.copy()
        offspring[2*i].set_allel(parent1.copy())
        offspring[2*i].set_fitness(fitness(parent1))
        offspring[2*i+1].set_allel(parent2.copy())
        offspring[2*i+1].set_fitness(fitness(parent2))
    return offspring

def mutation(pops):
    num_of_gen = len(pops)*cf.get_dimension()
    num_of_mutated_gen = int(cf.get_Pm()*num_of_gen)
    select = []
    copy_pops = []
    num_of_pops = len(pops)
    
    if num_of_mutated_gen > 0:
        #copy all offspring's chromosome & select random gen
        for i in range(num_of_gen):
            if i < num_of_pops: copy_pops.append(pops[i].get_allel().copy())
            select.append(rand.randint(0,(num_of_mutated_gen-1)))
        
        #select gen to be mutated
        for k in select:
            x = k//cf.get_dimension()
            y = k%cf.get_dimension()
            copy_pops[x][y] = rand.randint(0,(cf.get_maxallel()-1))
        
        #set back to original individu object
        for i in range(num_of_pops):
            pops[i].set_allel(copy_pops[i].copy())
            pops[i].set_fitness(fitness(copy_pops[i].copy()))
        
    return pops        

def replacement(old, new, size=cf.get_popsize()):
    new.extend(old)
    new = sorted(new, reverse=True, key=lambda ID: ID.get_fitness())
    return new[:size]

def abandon_egg(pops):
    for i in range(len(pops)):
        p = np.random.rand()
        if p < cf.get_Pa():
            allel, fitness = pops[i].new_egg()
            pops[i].set_allel(allel)
            pops[i].set_fitness(fitness)
    return pops
