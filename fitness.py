#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 13:47:10 2019

@author: cdjodistiara
"""

import pandas as pd
import numpy as np

beta = 200
gamma = 1

data_matkul = pd.read_excel('data/data.xlsx', sheet_name='dataS1', \
                            header=0, index_col=1).reset_index(drop=True)
data_ruang = pd.read_excel('data/data.xlsx', sheet_name='KAPASITAS', \
                          header=0).drop(0, axis=0).reset_index(drop=True)

dosen = data_matkul["KodePengj1"]
listdosen = set(dosen)
sks = data_matkul["SKS"]
kelas = data_matkul["Klas"]
jenis = data_matkul["Jenis"]
matkul = np.arange(len(data_matkul))
peserta = data_matkul["Peserta"]
kapasitas = data_ruang["kapa-sitas"]

jml_matkul = len(data_matkul)
jml_ruang = len(data_ruang)
jml_timeslot = jml_ruang*((5*10)-2)

def fitness(chromosome):
    value = 146292-(beta*hard(chromosome)+gamma*soft(chromosome))
    return value

def hard(chromosome):
    value = (np.sum(cekdosen(chromosome)) + \
             np.sum(cekmatkulwajib(chromosome)) +\
             np.sum(cekruangan(chromosome)) +\
             np.sum(cekkapasitas(chromosome)) +\
             np.sum(cekjenisruang(chromosome)))
    return value

def soft(chromosome):
    value = 0
    return value


#fungsi2 perbagiannya --- belom mempertimbangkan jumlah sks
#baru kepikiran, buat sks bisa di-append di list baru 'seen' sekalian append timeslot sesuai jumlah sksnya

# create array to check which gene violates the rule
def check(chromosome):
    checker = []
    seen = []
    for gen in chromosome: 
        checker.append(int(gen in seen))
        seen.append(gen)
    return checker

# convert to time -- time checker
def waktu(chromosome):
    global jml_ruang
    time = chromosome//(jml_ruang)
    return time

# convert to room -- room checker
def ruangan(chromosome):
    global jml_ruang
    room = chromosome%(jml_ruang)
    return room

#HARD CONSTRAINT #1 dosen -- DONE!
def cekdosen(chromosome):
    global dosen
    global listdosen
    checker = []
    cek_dosen = {dosenn: [] for dosenn in listdosen}
    timeslot = waktu(chromosome)
    for i, slot in enumerate(timeslot):
        checker.append(int(slot in cek_dosen[dosen[i]]))
        cek_dosen[dosen[i]].append(slot)
        if (sks[i] >= 2) or (sks[i] == 1 and jenis[i] == "PRAK"): 
            cek_dosen[dosen[i]].append(slot+1)
        if sks[i] == 3: cek_dosen[dosen[i]].append(slot+2)
    return checker

#HARD CONSTRAINT #2 cek matkul wajib -- blm sks, blm kelas a b iup
def cekmatkulwajib(chromosome):
    jml_matkulwajib = len(jenis[jenis == 'W'])
    slot = waktu(chromosome[:jml_matkulwajib])
    checker = check(slot)
    checker.extend(np.zeros(jml_matkul-len(checker)))
    return checker

#HARD CONSTRAINT #3 cek ruangan -- DONE!
def cekruangan(chromosome):
    checker = []
    seen = []
    for i, gen in enumerate(chromosome):
        checker.append(int(chromosome[i] in seen))
        seen.append(chromosome[i])
        if (sks[i] >= 2) or (sks[i] == 1 and jenis[i] == "PRAK"): 
            seen.append(chromosome[i]+jml_ruang)
        if sks[i] == 3: seen.append(chromosome[i]+(jml_ruang*2))
    return checker

#HARD CONSTRAINT #4 cek kapasitas ruangan -- DONE
def cekkapasitas(chromosome):
    global kapasitas
    global peserta
    checker = []
    rooms = ruangan(chromosome)
    for i, room in enumerate(rooms):
        checker.append(int(kapasitas[room] < peserta[i]))
    return checker

#HARD CONSTRAINT #5 -- DONE!
def cekjenisruang(chromosome):
    checker = []
    ruang = ruangan(chromosome)
    for matkul, gen in enumerate(chromosome): 
        prak = jenis[matkul] == 'PRAK'
        if prak: checker.append(int(ruang[matkul] < 22)) #27 -> num_of_room
        else: checker.append(int(ruang[matkul] >= 22))
    return checker