# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 15:12:53 2019

Graco

@author: tangk
"""

import os 
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
directories = ['Q:\\2018\\18-3000\\18-3010 (GRACO)\\',
               'Q:\\2017\\17-3000\\17-3010 (GRACO)\\',
               'Q:\\2016\\16-7000\\16-7010 (Graco)\\',
               'Q:\\2015\\15-7000 (incomplet)\\15-7010 (Graco) INCOMPLET\\',
               'Q:\\2014\\14-7000 (sauf 14-7062)\\14-7010 (Graco)\\',
               'Q:\\2013\\13-7000\\13-7010 (Graco)\\']
table = pd.DataFrame()

for d in directories:
    tests = glob.glob(d + '*.xlsx')
    for t in tests:
        single_table = pd.read_excel(t, header=1)
        single_table['Year'] = int(d[3:7])
        table = table.append(single_table)


table = table.rename(lambda x: x.replace('\n',' '), axis=1)
table = table.rename(lambda x: x.replace(' ', '_'), axis=1)
table = table.rename({'Unnamed:_31': 'Setup_Notes','Unnamed:_32': 'Results_Notes'}, axis=1)
table = table.dropna(axis=0, how='all')
table = table.dropna(axis=1, how='all')
table = table.reset_index()
#%%
subset = (table.query('Seat_Orientation==\'FORWARD\'')
               .query('Seat_secured_with==\'TYPE 2 BELT\'')
               .query('Dummy==\'HYBRID III 6Y\' or Dummy==\'HYBRID III 6Y (W)\'')
               .dropna(axis=1, how='all'))

subset['MODE'] = np.nan

low_back = [subset['Setup_Notes'].apply(lambda x: 'low back' in str(x).lower()),
            subset['Setup_Notes'].apply(lambda x: 'backless' in str(x).lower()),
            subset['Setup_Notes'].apply(lambda x: 'without back' in str(x).lower()),
            subset['Setup_Notes'].apply(lambda x: 'no back' in str(x).lower()),
            subset['Setup_Notes'].apply(lambda x: ' hb ' in str(x).lower())]

high_back = [subset['Setup_Notes'].apply(lambda x: 'highback' in str(x).lower()),
             subset['Setup_Notes'].apply(lambda x: 'high back' in str(x).lower()),
             subset['Setup_Notes'].apply(lambda x: 'with back' in str(x).lower()),
             subset['Setup_Notes'].apply(lambda x: ' lb ' in str(x).lower())]

subset.loc[pd.concat(low_back, axis=1).any(axis=1), 'MODE'] = 'LOW_BACK'
subset.loc[pd.concat(high_back, axis=1).any(axis=1), 'MODE'] = 'HIGH_BACK'

#%%
subset = subset.loc[~subset['MODE'].isna()]
subset.groupby(['Dummy','Test_Type','Model','MODE','Year']).mean()['Chest_Clip_3ms']
subset.groupby(['Dummy','Test_Type','MODE','Year']).mean()['Chest_Clip_3ms']
