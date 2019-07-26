# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 09:56:52 2019

@author: tangk
"""

from PMG.read_data import PMGDataset
from PMG.COM.helper import is_all_nan
import pandas as pd
import numpy as np


directory = 'P:\Data Analysis\Projects\Misc\ARS_Request\\'
cutoff = range(100, 1600)
channels = ['11HEAD0000THACXA',
            '11HEAD0000THACYA',
            '11HEAD0000THACZA',
            '11HEAD0000THAVXD',
            '11HEAD0000THAVYD',
            '11HEAD0000THAVZD',
            '13HEAD0000THACXA',
            '13HEAD0000THACYA',
            '13HEAD0000THACZA',
            '13HEAD0000THAVXD',
            '13HEAD0000THAVYD',
            '13HEAD0000THAVZD']
table_filters = {'drop': ['TC05-254',
                          'TC14-003',
                          'TC14-237',
                          'TC15-127',
                          'TC17-001',
                          'TC13-110',
                          'TC15-504',
                          'TC16-021',
                          'TC16-018',
                          'TC11-504',
                          'TC15-017']} # these have THOR but are not in the data file
preprocessing = None


#%% initialize the dataset and specify channels, filters, and preprocessing
dataset = PMGDataset(directory, channels=channels, cutoff=cutoff, verbose=False)
dataset.table_filters = table_filters
dataset.preprocessing = preprocessing
dataset.get_data(['timeseries'])

#%% get info
info_table = pd.concat(((dataset.table['ID11']
                                .reset_index()
                                .query('ID11==\'THOR\'')
                                .replace('THOR','Driver')
                                .rename({'ID11': 'Position'}, axis=1)),
                        (dataset.table['ID13']
                                .reset_index()
                                .query('ID13==\'THOR\'')
                                .replace('THOR','Passenger')
                                .rename({'ID13': 'Position'}, axis=1)))).reset_index(drop=True)
info_table['Year'] = dataset.table.loc[info_table['TC'], 'Year'].values
info_table['Model'] = dataset.table.loc[info_table['TC'],'Model'].values
info_table['Config'] = '40% Frontal Offset'
info_table['Vehicle Type'] = np.nan
info_table['Speed'] = dataset.table.loc[info_table['TC'],'Speed'].values
info_table['Restraint'] = np.nan
info_table['Data_type'] = '3 ACC + 3 ARS'

info_table = info_table.sort_values(['Year','TC'])
info_table.to_csv(directory + 'info_table.csv')

