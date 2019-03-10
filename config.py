#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:09:13 2019

@author: cdjodistiara
"""

class Config:
    #===========chromosomes n pops=============
    __Popsize = 10
    __Maxgen = 5
    __NumOfCourse = 15
    __NumOfClass = 10
    __NumOfTimeslots = 2
    # __MaxAllel = __NumOfClass * __NumOfTimeslots
    __MaxAllel = 100
    __MinAllel = 1
    #=======cuckoo=========
    __Lambda = 1.5
    __Alpha = 0.01
    __Pa = 0.2
    #=========GA==========
    __Pc = 0.8
    __Pm = 0.1
    __Num_of_pointer = 4
    __K_mutation = 2
    __K_crossover = 4


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
    def get_numofpointer(self):
        return self.__Num_of_pointer

    @classmethod
    def get_kmut(self):
        return self.__K_mutation

    @classmethod
    def get_kcross(self):
        return self.__K_crossover

    @classmethod
    def get_dimension(self):
        return self.__NumOfCourse

    # @classmethod
    # def set_dimension(self, _dimension):
    #     self.__NumOfCourse = _dimension

    @classmethod
    def get_maxallel(self):
        return self.__MaxAllel

    @classmethod
    def get_minallel(self):
        return self.__MinAllel
