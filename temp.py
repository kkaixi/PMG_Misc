# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 09:14:15 2019

@author: tangk
"""

import xlwings as xw
import os
from PMG.read_data import PMGDataset

col_names = ['T_10000_0',
              '10SIMELE00INACXD',
              '10SIMERI00INACXD',
              '10CVEHCG0000ACXD',
              '10CVEHCG0000ACYD',
              '10CVEHCG0000ACZD',
              '11HEAD0000THACXA',
              '11HEAD0000THACYA',
              '11HEAD0000THACZA',
              '11HEAD0000THAVXA',
              '11HEAD0000THAVYA',
              '11HEAD0000THAVZA']

directory = 'P:\\Data Analysis\\Tests for Suzanne\\THOR ARS Data\\Tests\\'
dataset = PMGDataset(directory, channels=['10SIMELE00INACXD','10CVEHCG0000ACXD'], cutoff=range(100))
dataset.get_data(['timeseries'])

tcs = os.listdir(directory)

for tc in tcs:
    if tc=='Table.csv' or tc=='Test & data ID.xlsx': continue
    book = xw.Book(directory + tc)
    sheet = book.sheets[0]
    cols = sheet.range('B1:M1').value
    
    # check columns
    if any([col_names[i] != cols[i] for i in range(len(col_names))]):
        print('Columns missing in ' + tc)
    
    y1 = np.array(sheet.range('C4').expand('down').value[:100])
    y2 = dataset.timeseries.at[tc[:8], '10SIMELE00INACXD']
    
    if np.any(np.abs(y1-y2)>0.01):
        print('SIME Values do not match for ' + tc)
        
    y1 = np.array(sheet.range('E4').expand('down').value[:100])
    y2 = dataset.timeseries.at[tc[:8], '10CVEHCG0000ACXD']
    
    if np.any(np.abs(y1-y2)>0.01):
        print('VEHCG Values do not match for ' + tc)
        break
    
    book.close()
    
    
    
    
    
    