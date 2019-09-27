#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 15:42:36 2019

@author: cdjodistiara
"""
from time import time
from config import Config as cf
import individu as idv
from matplotlib import pyplot as plt
plt.switch_backend('agg')
import sys
from fitness import fitness_eval
import csv

def main_algo(algo="hybrid", trials=5, project=""):
    print("\nRunning " + algo + "...")
    plt.figure(figsize=(16,8))
    plt.xlabel('Generasi', fontsize=14)
    plt.ylabel('Fitness', fontsize=14)
    if project == "Pc" or project == "Pm" or project == "Pa":
        plt.title('Grafik Uji Parameter ' + project + ' (' + algo + ')', fontsize=18)
        if project == "Pc":
            print("Pc: ", cf.get_Pc())
        elif project == "Pm":
            print("Pm: ", cf.get_Pm())
        elif project == "Pa":
            print("Pa: ", cf.get_Pa())
        elif project == "Ukuran Populasi":
            print("Pops: ", cf.get_popsize())
    elif project == "":
        plt.title('Grafik performa algoritme (' + algo + ')', fontsize=18)
    plt.ylim(0, 120000)
    best_trials = []
    rec = []
    try:
        for trial in range(trials):
            algo = algo.lower()
            if algo == 'hybrid': label = 'HYBRID'
            elif algo == 'ga': label = 'Algoritme Genetika'
            first = time()
            pops = []
            best = []
            convergence = False
            t = 0
            r = 0

            for i in range(cf.get_popsize()):          # create initial
                pops.append(idv.Individu())             # population
                pops[i].set_fitness()    

            #====================START ITERATION=======================
            # while (not convergence or r < 970):
            while (not convergence or t < cf.get_maxgen()):

                if algo=="hybrid" or algo=="ga":
                    parent = idv.selection(pops)              # selection
                    new_pops = idv.crossover(parent)          # crossover
                    new_pops = idv.mutation(new_pops)         # mutation
                
                if algo=="cs": new_pops = pops.copy()
        
                if algo=="hybrid" or algo=="cs":
                    new_pops = idv.replace_egg(new_pops)  # replace host egg
                    new_pops = idv.abandon_egg(new_pops)  # replace worst egg
        
                pops = idv.replacement(pops, new_pops, algo)  # elitism
                r = time() - first
                best.append(pops[0].get_fitness())
                sys.stdout.write("\rGeneration:%d, BestFitness:%d, Runtime:%f"\
                                 % (t, best[t], r))
                if t > 100:
                    convergence = bool(best[t] == best[t-100])
                t = t + 1

            print("")
            #================Save log, graph, and result================
            rec.append([best[t-1], r])
            plt.plot(best, label=str(trial+1))
            best_trials.append(best)
            fitness_eval(pops[0], algo)            
            file = 'result/' + project + cf.filename() + '(' + algo + str(best[t-1]) + ').csv'
            with open(file, 'wt') as f:
                writer = csv.writer(f)
                writer.writerow(best)
        #=========================END TRIAL=========================
        plt.legend(loc='best')
        plt.savefig('result/' + project + cf.filename() + '(' + algo + str(best[t-1]) + ').jpg')
        return best_trials
    except KeyboardInterrupt:
        file = 'result/' + project + '_aborted_' + cf.filename() + '(' + algo + str(best[t-1]) + ').csv'
        with open(file, 'wt') as f:
            writer = csv.writer(f)
            writer.writerow(best)
        best_trials.append(best)
        fitness_eval(pops[0], algo)
        plt.plot(best, label=str(trial+1))
        plt.legend(loc='best')
        plt.savefig('result/' + project + '_aborted_' +  cf.filename() + '(' + algo + str(best[t-1]) + ').jpg')
        return best_trials

if __name__ == "__main__":
    cf.set_Pc(0.8)
    cf.set_Pm(0.05)
    cf.set_Pa(0.4)
    cf.set_maxgen(100)
    size = [100, 200]
    #algo = ["GA", "Hybrid"]
    algo = ["Hybrid", "GA"]
    for i in range(len(size)):
        cf.set_popsize(size[i])
        res = main_algo(algo=algo[i], trials=5, project="")
        plt.figure(figsize=(16,8))
        plt.ylim(0, 120000)
        plt.xlabel('Generasi', fontsize=14)
        plt.ylabel('Fitness', fontsize=14)
        plt.title('Grafik Uji Ukuran Populasi (' + algo[i] + ')', fontsize=18)
        avg_best = [sum(row)/len(row) for row in list(map(list, zip(*res)))]
        for best in res: plt.plot(avg_best)
        plt.savefig('result/popsize_' + cf.filename() + '(' + algo[i] + ').jpg')