#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:09:13 2019

@author: cdjodistiara
"""
from fitness import jml_timeslot, jml_matkul

class Config:
    #===========chromosomes n pops=============
    __Popsize = 10
    __Maxgen = 300
    __Dimension = jml_matkul
    __MaxAllel = jml_timeslot
    __MinAllel = 0
    #=======cuckoo=========
    __Lambda = 1.5
    __Alpha = 0.1
    __Pa = 0.1
    #=========GA==========
    __Pc = 0.8
    __Pm = 0.1
    __K_crossover = 10
    __K_mutation = 10


    @classmethod
    def get_popsize(self):
        return self.__Popsize

    @classmethod
    def get_Pa(self):
        return self.__Pa

    @classmethod
    def get_Pc(self):
        return self.__Pc

    @classmethod
    def get_Pm(self):
        return self.__Pm

    @classmethod
    def get_lambda(self):
        return self.__Lambda

    @classmethod
    def get_alpha(self):
        return self.__Alpha

    @classmethod
    def get_maxgen(self):
        return self.__Maxgen

    @classmethod
    def get_kmut(self):
        return self.__K_mutation

    @classmethod
    def get_kcross(self):
        return self.__K_crossover

    @classmethod
    def get_dimension(self):
        return self.__Dimension

    @classmethod
    def get_maxallel(self):
        return self.__MaxAllel

    @classmethod
    def get_minallel(self):
        return self.__MinAllel