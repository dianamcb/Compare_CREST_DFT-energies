#!/usr/bin/python
#Author: disa
#Description: This code make and sort the table of energies of the comparison between the energies give by CREST and DFT. This tables can be open in excel/Google sheets (file->import->select the file->insert new sheet)
#Instructions: To execute this code, python3 compare_energies.py [path of folder of CREST/] [path of the folder of DFT/] !!!This paths are the direction is where we first extract the energies of CREST and DFT [e.g: ../Extract-energies-CREST/out-folder_name]

import numpy as np
import pandas as pd
import os, re, sys

# Necesita los dos path the crest y dft30
argv = sys.argv
path_crest = argv[1]
path_dft30 = argv[2]

# Entra y busca el .dat en ambas carpetas
for fileName in os.listdir(path_crest):
    if fileName.endswith('.dat'): 
        data_crest = pd.read_csv(f'{path_crest}{fileName}',sep='\t')
        data_crest['CREST-Energy[kcal/mol]'] = data_crest['Energy[kcal/mol]'].map('{:.4f}'.format)
        data_crest.sort_values('Energy[kcal/mol]',ignore_index=True,inplace=True)

for fileName in os.listdir(path_dft30):
    if fileName.endswith('.dat'): 
        data_dft30 = pd.read_csv(f'{path_dft30}{fileName}',sep='\t')
        data_dft30['DFT-Energy[kcal/mol]'] = data_dft30['Energy[kcal/mol]'].map('{:.4f}'.format)
        data_dft30.sort_values('Energy[kcal/mol]',ignore_index=True,inplace=True)

# Concatenate both tables
data = pd.concat([data_dft30[['File number','DFT-Energy[kcal/mol]']],data_crest['CREST-Energy[kcal/mol]']],axis=1)
data.rename(columns={'File number':'conformers'},inplace=True)
#data['Abs err[kcal/mol]'] = abs(data_crest['Energy[kcal/mol]']-data_dft30['Energy[kcal/mol]'])
data['\u0394E_dft30[kcal/mol]'] = data_dft30['Energy[kcal/mol]']-data_dft30['Energy[kcal/mol]'].min()
data['\u0394E_crest[kcal/mol]'] = data_crest['Energy[kcal/mol]']-data_crest['Energy[kcal/mol]'].min()
print(data)
data.sort_values('DFT-Energy[kcal/mol]',ignore_index=True,ascending=False,inplace=True) #Sort table from the lowest dft energy value to highest
# print(data_dft30['Energy[kcal/mol]'].min())
# data['Abs err[kcal/mol]'] = data['Abs err[kcal/mol]'].map('{:.4f}'.format)
data = data[['conformers', '\u0394E_crest[kcal/mol]', '\u0394E_dft30[kcal/mol]']]
# print(data)
data[:30].to_csv('first30-energies.csv',sep=',', float_format='%.4f', index=False)
data.to_csv('all-energies.csv',sep=',', float_format='%.4f', index=False)
data[:30].to_csv('V-first30-energies.dat',sep='\t', float_format='%.4f', index=False)
data.to_csv('V-all-energies.dat',sep='\t', float_format='%.4f', index=False)
 
