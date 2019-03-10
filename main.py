#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:42:36 2019

@author: cdjodistiara
"""

from config import Config as cf
import individu as idv
import random as rand
# import function as fx 


def show_all(pops):
  for i in range(len(pops)):
    print("[", i, "] -> ", pops[i].get_allel(), " - f: ", pops[i].get_fitness())

def main():
    pops = []
#    best = []
    #================create initial population=============
    # num of id: cf.get_popsize()
    for id in range(cf.get_popsize()): pops.append(idv.Individu())
    
    print("initial population: ")
    show_all(pops)
    #================calculate fitness=====================
#    pops = sorted(pops, reverse=True, key=lambda ID: ID.get_fitness())
#     current_best = pops[0].get_fitness()
    
#     print(pops[0])
#     print(current_best)

    for t in range(cf.get_maxgen()):
        print("===============GEN ", t, "================")
        #================crossover==========================
        select = idv.selection(pops)
        print("selected from RWS: ")
        show_all(select)
        selected, num = idv.select_individuals(select, cf.get_Pc())
        print("selected from Pc: ", num)
        show_all(selected)
        if num:
            new_pops = idv.crossover(selected)
            print("offsprings: ")
            show_all(new_pops)
            
            #=======================mutation====================
            select_from_pm, num2 = idv.select_individuals(new_pops, cf.get_Pm())
            for index in num2: new_pops[index].mutate()
    
            #====================cuckoo search==================
            #create new egg from best individual
            new_pops = sorted(new_pops, reverse=True, key=lambda ID: ID.get_fitness())
            print("best: ", new_pops[0].get_allel())
            allel, fitness = new_pops[0].new_egg()
            print("cuckoo egg: ", allel)
    
            #check random egg then review the fitness value
            r = rand.randint(0, len(new_pops)-1)
            print("chosen individual: ", new_pops[r].get_allel())
            if fitness > new_pops[r].get_fitness():
                new_pops[r].set_allel(allel)
                new_pops[r].set_fitness(fitness)
            
            #abandoned egg get replaced
            new_pops = idv.abandon_egg(new_pops)
            
            #=============generational replacement==============
            pops = idv.replacement(pops, new_pops)
        
        print("new pops: ")
        show_all(pops)

main()
