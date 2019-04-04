#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:42:36 2019

@author: cdjodistiara
"""
from time import time
from config import Config as cf
import individu as idv
import random as rand
from matplotlib import pyplot as plt
import sys
from fitness import fitness

best_individuals = []
best_fitness = []

def show_all(pops, text=""):
    print(text)
    for i in range(len(pops)):
        print("[", i, "] -> ", pops[i].get_fitness())

def main(hybrid=False, GA=False, CS=False):
    first = time()
    pops = []
    best = []
    
    for i in range(cf.get_popsize()):           #create initial population
        pops.append(idv.Individu())
        pops[i].set_fitness(fitness(pops[i].get_allel()))
    
    #====================START ITERATION=======================
    for t in range(cf.get_maxgen()):
        if hybrid or GA:
            parent = idv.selection(pops)        # selection
            new_pops = idv.crossover(parent)    # crossover
            new_pops = idv.mutation(new_pops)   # mutation
            
        if CS: new_pops = pops.copy()
        
        if hybrid or CS:
            new_pops = sorted(new_pops, reverse=True, \
                              key=lambda ID: ID.get_fitness())  # create new egg
            allel, fitnessvalue = new_pops[0].new_egg()
            
            r = rand.randint(0, len(new_pops)-1)
            if fitnessvalue > new_pops[r].get_fitness(): # replace if new egg
                new_pops[r].set_allel(allel)             # is better
                new_pops[r].set_fitness(fitnessvalue)

            new_pops = idv.abandon_egg(new_pops)        # replace abandoned egg
    #=====================END ITERATION========================
        
        pops = idv.replacement(pops, new_pops)      # elitism
        best.append(pops[0].get_fitness())
        sys.stdout.write("\rGeneration:%d, BestFitness:%d" % (t, best[t]))
    
    print("Runtime : ", time()-first)
    print("best fitness : ", best[cf.get_maxgen()-1])
    print("best chromosome: ")
    print(pops[0].get_allel())
    if hybrid: color='r-'
    elif GA: color='b-' 
    elif CS: color='g-'
    plt.plot(best, color)

plt.figure(figsize=(10,7))
plt.xlabel('Generations')
plt.ylabel('Best fitness')

print("Running hybrid algorithm...")
main(hybrid=True)
print("\n\nRunning genetic algorithm...")
main(GA=True)

plt.legend(['Hybrid', 'GA only'])
plt.title('Performance Graph')

plt.legend("Hybrid", "GA")
plt.show()
