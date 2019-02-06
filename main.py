from config import Config as cf
import individu as idv
# import function as fn 

import numpy as np

def main():
    pops = []
    best = []
    #================create initial population=============
    # num of id: cf.get_popsize()
    for id in range(cf.get_popsize()): pops.append(idv.Individu())
    
    #================calculate fitness=====================
    pops = sorted(pops, reverse=True, key=lambda ID: ID.get_fitness())
    current_best = pops[0].get_fitness()
    
    print(pops[0])
    print(current_best)

    for t in range(cf.get_maxgen()):
        #================crossover==========================
        select_from_pc, num = idv.select_individuals(pops, cf.get_Pc())
        selection = idv.selection(select_from_pc, cf.get_pointer())
        new_pops = idv.crossover(selection)

        #=======================mutation====================
        select_from_pm, num = idv.select_individuals
        new_pops = idv.mutation(new_pops, num)


        #====================cuckoo search==================


        #=============generational replacement==============
        pops = idv.replacement(new_pops)

main()
