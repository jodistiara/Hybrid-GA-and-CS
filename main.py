from config import Config as cf
import individu as idv
# import function as fx 

import numpy as np

def main():
    pops = []
    best = []
    #================create initial population=============
    # num of id: cf.get_popsize()
    for id in range(cf.get_popsize()): pops.append(idv.Individu())
    
    #================calculate fitness=====================
    pops = sorted(pops, reverse=True, key=lambda ID: ID.get_fitness())
#     current_best = pops[0].get_fitness()
    
#     print(pops[0])
#     print(current_best)

    for t in range(cf.get_maxgen()):
        print("===============GEN ", t, "================")
        #================crossover==========================
        select_from_pc, num = idv.select_individuals(pops, cf.get_Pc())
        selection = idv.selection(select_from_pc, cf.get_pointer())
        new_pops = idv.crossover(selection)

        #=======================mutation====================
        select_from_pm, num = idv.select_individuals(new_pops, cf.get_Pm())
        for index in num: new_pops[index].mutate()

        #====================cuckoo search==================
        #create new egg from best individual
        new_pops = sorted(new_pops, reverse=True, key=lambda ID: ID.get_fitness())
        allel, fitness = new_pops[0].new_egg()

        #check random egg then review the fitness value
        r = rand.randint(0, len(new_pops)-1)
        if fitness > new_pops[r].get_fitness():
                new_pops[r].set_allel(allel)
                new_pops[r].set_fitness(fitness)

        new_pops = sorted(new_pops, reverse=True, key=lambda ID: ID.get_fitness())
        
        #=============generational replacement==============
        pops = idv.replacement(new_pops)

main()
