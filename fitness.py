#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 13:47:10 2019

@author: cdjodistiara
"""

import pandas as pd
import numpy as np
import pickle

beta = 600
eps = 1

data_matkul = pd.read_excel('data/data.xlsx', \
                            sheet_name='dataS1', \
                            header=0, \
                            index_col=1).reset_index(drop=True)
# data_ruang = pd.read_excel('data/data.xlsx', \
#                            sheet_name='KAPASITAS', \
#                            header=0).drop(0,axis=0).reset_index(drop=True)

# with(open('data/data_matkul.pkl', 'rb')) as f:
#     data_matkul = pickle.load(f)
with(open('data/data_ruang.pkl', 'rb')) as f:
    data_ruang = pickle.load(f)
    
dosen1 = data_matkul["KodePengj1"]
dosen2 = data_matkul["KodePengj2"]
dosen = list(dosen1.copy())
dosen.extend([x for x in dosen2 if str(x) != 'nan'])
listdosen = set(dosen)
tim = [x == x for x in dosen2]
sks = data_matkul["SKS"]
kelas = data_matkul["Klas"]
listkelas = set(kelas)
jenis = data_matkul["Jenis"]
matkul = np.arange(len(data_matkul))
smt = data_matkul["Sem"]
listsmt = set(smt)
peserta = data_matkul["Peserta"]
kapasitas = data_ruang["kapa-sitas"]
ruang_kelas = data_ruang["ruangan"]

jml_matkul = len(data_matkul)
jml_ruang = len(data_ruang)
jml_slot_perminggu = (5*10)-2
total_slot = jml_ruang*jml_slot_perminggu

def fitness(chromosome):
    value = (beta*hard(chromosome)+eps*soft(chromosome))
    return int(value)

def hard(chromosome):
    value = (np.sum(cekdosen(chromosome)) + \
             np.sum(cekwajib(chromosome)) +\
             np.sum(cekruangan(chromosome)) +\
             np.sum(cekkapasitas(chromosome)) +\
             np.sum(cekjenisruang(chromosome)) +\
             np.sum(ceksemester(chromosome)))
    return value

def soft(chromosome):
    value = (np.sum(kelasparalel(chromosome)) + \
             np.sum(ruangvskapasitas(chromosome)) + \
             np.sum(max8sks(chromosome)))
    return value

#HARD CONSTRAINT #1 dosen -- udah sama SKS
def cekdosen(chromosome):
    violate = []
    cek_dosen = {dosenn: [] for dosenn in listdosen}
    timeslot = [gen//(jml_ruang) for gen in chromosome]
    for i, slot in enumerate(timeslot):
        if not tim[i]:
            exist = 0
            if slot in cek_dosen[dosen1[i]]: exist = 1
            cek_dosen[dosen1[i]].append(slot)
            if (sks[i] >= 2) or (sks[i] == 1 and jenis[i] == "PRAK"): 
                if (slot+1) in cek_dosen[dosen1[i]]: exist = 1
                cek_dosen[dosen1[i]].append(slot+1)
            if sks[i] == 3: 
                if (slot+2) in cek_dosen[dosen1[i]]: exist = 1
                cek_dosen[dosen1[i]].append(slot+2)
        else:
            if (slot+1) in cek_dosen[dosen1[i]]: exist = 1
            if (slot+1) in cek_dosen[dosen2[i]]: exist = 1
            cek_dosen[dosen1[i]].append(slot)
            cek_dosen[dosen2[i]].append(slot)
            if (sks[i] == 2) or (sks[i] == 1 and jenis[i] == "PRAK"): 
                if (slot+1) in cek_dosen[dosen1[i]] or (slot+1) in cek_dosen[dosen2[i]]: exist = 1
                cek_dosen[dosen1[i]].append(slot+1)
                cek_dosen[dosen2[i]].append(slot+1)
            elif sks[i] == 3: 
                if (slot+1) in cek_dosen[dosen1[i]] or (slot+1) in cek_dosen[dosen2[i]]: exist = 1
                cek_dosen[dosen1[i]].append(slot+1)
                cek_dosen[dosen2[i]].append(slot+1)
                if (slot+2) in cek_dosen[dosen1[i]] or (slot+2) in cek_dosen[dosen2[i]]: exist = 1
                cek_dosen[dosen1[i]].append(slot+2)
                cek_dosen[dosen2[i]].append(slot+2)
        violate.append(exist)
    return violate

#HARD CONSTRAINT #2 cek matkul wajib -- udah sama SKS
def cekwajib(chromosome):
    violate = []
    cek_kelas = {kelass: [] for kelass in listkelas}
    chromosome = chromosome[jenis[jenis != 'P'].index]
    timeslot = [gen//(jml_ruang) for gen in chromosome]
    for i, slot in enumerate(timeslot):
        slot = [slot, slot+1]
        if (sks[i] == 2) or (sks[i] == 1 and jenis[i] == "PRAK"):
        	violate.append(int(bool([x for x in slot if x in cek_kelas[kelas[i]]])))
        	cek_kelas[kelas[i]].extend(slot)
        elif sks[i] == 3:
        	slot.append(slot[0]+2)
        	violate.append(int(bool([x for x in slot if x in cek_kelas[kelas[i]]])))
        	cek_kelas[kelas[i]].extend(slot)
    violate.extend(np.zeros(jml_matkul-len(violate), dtype=np.int8))
    return violate

#HARD CONSTRAINT #3 -- udah SKS
def ceksemester(chromosome):
    violate = []
    from collections import defaultdict
    cek_kelas = defaultdict(lambda: defaultdict(list))
    timeslot = [gen//(jml_ruang) for gen in chromosome]
    for i, slot in enumerate(timeslot):
        smstr = []
        smstr.append(slot)
        if (sks[i] == 2) or (sks[i] == 1 and jenis[i] == "PRAK"): 
            smstr.append(slot+1)
        if sks[i] == 3: 
        	smstr.append(slot+1)
        	smstr.append(slot+2)
        collides = False
        for t in smstr:
            if kelas[i] == 'IUP':
                if t in cek_kelas['IUP1'][smt[i]]: collides = True
                if t in cek_kelas['IUP2'][smt[i]]: collides = True
                cek_kelas['IUP1'][smt[i]].append(t)
                cek_kelas['IUP2'][smt[i]].append(t)
            elif kelas[i] == 'ILKOM' or (kelas[i] != 'IUP1' and \
                    kelas[i] != 'IUP2' and jenis[i] == 'PRAK'):
                if t in cek_kelas['A'][smt[i]]: collides = True
                if t in cek_kelas['B'][smt[i]]: collides = True
                cek_kelas['A'][smt[i]].append(t)
                cek_kelas['B'][smt[i]].append(t)
            else:
                if t in cek_kelas[kelas[i]][smt[i]]:
                    collides = True
                cek_kelas[kelas[i]][smt[i]].append(t)
        violate.append(int(collides))
    return violate

#HARD CONSTRAINT #4 cek ruangan -- udah SKS
def cekruangan(chromosome):
    violate = []
    seen = []
    for i, gen in enumerate(chromosome):
        slot = [gen, gen+jml_ruang]
        if (sks[i] == 2) or (sks[i] == 1 and jenis[i] == "PRAK"): 
            violate.append(int(bool([x for x in slot if x in seen])))
            seen.extend(slot)
        if sks[i] == 3: 
            slot.append(gen+(jml_ruang*2))
            violate.append(int(bool([x for x in slot if x in seen])))
            seen.extend(slot)
    return violate

#HARD CONSTRAINT #5 cek kapasitas ruangan -- DONE
def cekkapasitas(chromosome):
    violate = []
    rooms = [gen%(jml_ruang) for gen in chromosome]
    for i, room in enumerate(rooms):
        violate.append(int(kapasitas[room] < peserta[i]))
    return violate

#HARD CONSTRAINT #6 -- DONE!
def cekjenisruang(chromosome):
    violate = []
    ruang = [gen%(jml_ruang) for gen in chromosome]
    for matkul, gen in enumerate(chromosome): 
        prak = jenis[matkul] == 'PRAK'
        if prak: violate.append(int(ruang[matkul] < 22))
        else: violate.append(int(ruang[matkul] >= 22))
    return violate

#SOFT CONSTRAINT #1 kelas paralel dijadwalkan bersamaan
def kelasparalel(chromosome):
    violate = []
    kodematkul = data_matkul['Kode']
    cek_matkul = {kode: [] for kode in kodematkul}
    timeslot = [gen//(jml_ruang) for gen in chromosome]
    for i, slot in enumerate(timeslot):
        if not cek_matkul[kodematkul[i]]:
            cek_matkul[kodematkul[i]].append(slot)
            violate.append(0)
        else:
            if slot in cek_matkul[kodematkul[i]]:
                violate.append(0)
            else:
                cek_matkul[kodematkul[i]].append(slot)
                violate.append(1)
    return violate

#SOFT CONSTRAINT #2 penggunaan ruang optimal
def ruangvskapasitas(chromosome):
    violate = []
    ruang = [gen%(jml_ruang) for gen in chromosome]
    for i in range(len(ruang)):
        if kapasitas[ruang[i]] > 30:
            minimal = 0.6
            maksimal = 0.9
        else: 
            minimal = 0.1
            maksimal = 1
        persentase = peserta[i]/kapasitas[ruang[i]]
        if persentase>=minimal and persentase<=maksimal:
            violate.append(0)
        else: violate.append(1)
    return violate

#SOFT CONSTRAINT #3 1 hari max 8 sks
def max8sks(chromosome):
    violate = []
    from collections import defaultdict
    cek_hari = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    slot = [x//(jml_ruang*10) for x in chromosome]
    
    for i in range(len(slot)):
        if kelas[i].lower() == 'iup':
            cek_hari['IUP1'][smt[i]][slot[i]].append(sks[i])
            cek_hari['IUP2'][smt[i]][slot[i]].append(sks[i])
            total = np.sum(cek_hari['IUP1'][smt[i]][slot[i]])
            if total < np.sum(cek_hari['IUP2'][smt[i]][slot[i]]):
               total = np.sum(cek_hari['IUP2'][smt[i]][slot[i]]) 
        elif kelas[i].lower() == 'ilkom':
            cek_hari['A'][smt[i]][slot[i]].append(sks[i])
            cek_hari['B'][smt[i]][slot[i]].append(sks[i])
            total = np.sum(cek_hari['A'][smt[i]][slot[i]])
            if total < np.sum(cek_hari['B'][smt[i]][slot[i]]):
               total = np.sum(cek_hari['B'][smt[i]][slot[i]])
        else:       
            cek_hari[kelas[i]][smt[i]][slot[i]].append(sks[i])
            total = np.sum(cek_hari[kelas[i]][smt[i]][slot[i]])
        
        if total > 8: violate.append(1)
        else: violate.append(0)
    return violate

def fitness_eval(individu, algo):
    gen = individu.get_allel()
    fitness = individu.get_fitness()
    value = []
    value.append(gen)
    value.append(cekdosen(gen))
    value.append(cekwajib(gen))
    value.append(cekruangan(gen))
    value.append(cekkapasitas(gen))
    value.append(cekjenisruang(gen))
    value.append(ceksemester(gen))
    value.append(kelasparalel(gen))
    value.append(ruangvskapasitas(gen))
    value.append(max8sks(gen))
    
    value = list(map(list, zip(*value)))
    
    fname = 'log/' + algo + '-' + str(fitness) + '-fitness_eval.xlsx'
    writer = pd.ExcelWriter(fname, engine = 'xlsxwriter')
    result = pd.DataFrame(value, columns=["gen", "dosen", "wajib", \
                                          "ruangan", "kapasitas", \
                                          "jenis ruangan", "semester", \
                                          "kelas paralel", \
                                          "persentase kapasitas", \
                                          "max sks 1 hari"])
    result.to_excel(writer, engine = 'xlsxwriter')
    writer.save()
    writer.close()

def print_schedule(individu, algo, detail=""):  
    chromosome = individu.get_allel()
    value = individu.get_fitness()
    schedule = pd.DataFrame(columns=np.arange(0,jml_slot_perminggu), \
                            index=ruang_kelas)
    time = [gen//(jml_ruang) for gen in chromosome]
    room = [gen%(jml_ruang) for gen in chromosome]
    
    for i in range(jml_matkul):
        course_info = []
        r = room[i]
        t = time[i]
        lect = dosen1[i]
        if tim[i]: lect = lect + ' & ' + dosen2[i]
        
        course_info.append(data_matkul['Mata Kuliah'][i])
        course_info.append(lect)
        course_info.append(kelas[i]+' (' +str(peserta[i])+' orang)')
        course_info = "\n".join(course_info)
        # course_info.append(jenis[i])
        # course_info.append(str(smt[i]))
        # course_info = "".join(course_info)
        
        #====sampe sini aman====
        
        if str(schedule[t][r]) == 'nan': schedule[t][r] = course_info
        else: schedule[t][r] = "\n".join([schedule[t][r], '-----------', course_info])
        
        if sks[i] >= 2 or jenis[i] == 'PRAK':
            t = t + 1
            if t < 48:
                if str(schedule[t][r]) == 'nan': 
                    schedule[t][r] = course_info
                else: schedule[t][r] = "\n".join([schedule[t][r], \
                             '-----------', course_info])
                if sks[i] > 2:
                    t = t + 1
                    if t < 48:
                        if str(schedule[t][r]) == 'nan': 
                            schedule[t][r] = course_info
                        else: 
                            schedule[t][r] = "\n".join([schedule[t][r], \
                                     '-----------', course_info])

    fname = 'result/' + detail + algo + '-' + str(value) + '-schedule.xlsx'
    writer = pd.ExcelWriter(fname, engine = 'xlsxwriter')
    schedule.to_excel(writer, engine='xlsxwriter')
    writer.save()
    writer.close()