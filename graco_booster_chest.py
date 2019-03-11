# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 15:12:53 2019

Graco

@author: tangk
"""

import os 
import re
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#%%
PATH = "P:/Data Analysis/Projects/Misc/Graco_Chest/"

directories = ['Q:\\2018\\18-3000\\18-3010 (GRACO)\\',
               'Q:\\2017\\17-3000\\17-3010 (GRACO)\\',
               'Q:\\2016\\16-7000\\16-7010 (Graco)\\',
               'Q:\\2015\\15-7000 (incomplet)\\15-7010 (Graco) INCOMPLET\\',
               'Q:\\2014\\14-7000 (sauf 14-7062)\\14-7010 (Graco)\\',
               'Q:\\2013\\13-7000\\13-7010 (Graco)\\']
#directories = ['P:\\2019\\19-6000\\19-6032 (213)\\',
#               'Q:\\2018\\18-6000\\18-6032 (213)\\',
#               'Q:\\2017\\17-6000\\17-6032 (213)\\',
#               'Q:\\2016\\16-6000\\16-6032 (213)\\',
#               'Q:\\2015\\15-6000 (incomplet)\\15-6032\\']
table = pd.DataFrame()

for d in directories:
    tests = glob.glob(d + '*Test*Results*.xlsx')
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
subset = (table.query('Make==\'GRACO\'')
               .query('Seat_Orientation==\'FORWARD\'')
               .query('Seat_secured_with==\'TYPE 2 BELT\'')
               .query('Dummy==\'HYBRID III 6Y\' or Dummy==\'HYBRID III 6Y (W)\'')
               .dropna(axis=1, how='all'))

subset['MODE'] = np.nan

low_back = [subset['Setup_Notes'].apply(lambda x: 'low back' in str(x).lower()),
            subset['Setup_Notes'].apply(lambda x: 'backless' in str(x).lower()),
            subset['Setup_Notes'].apply(lambda x: 'without back' in str(x).lower()),
            subset['Setup_Notes'].apply(lambda x: 'no back' in str(x).lower()),
            subset['Setup_Notes'].apply(lambda x: ' hb ' in str(x).lower()),
            subset['Model'].apply(lambda x: 'backless' in str(x).lower())]

high_back = [subset['Setup_Notes'].apply(lambda x: 'highback' in str(x).lower()),
             subset['Setup_Notes'].apply(lambda x: 'high back' in str(x).lower()),
             subset['Setup_Notes'].apply(lambda x: 'with back' in str(x).lower()),
             subset['Setup_Notes'].apply(lambda x: ' lb ' in str(x).lower())]

subset.loc[pd.concat(low_back, axis=1).any(axis=1), 'MODE'] = 'LOW_BACK'
subset.loc[pd.concat(high_back, axis=1).any(axis=1), 'MODE'] = 'HIGH_BACK'
subset = subset.loc[~subset['MODE'].isna()]
subset = subset.replace('TURBO BOOSTER BACKLESS','TURBO BOOSTER')
subset = subset.replace('AFFIX BACKLESS','AFFIX')
#subset = subset.query('Dummy==\'HYBRID III 6Y\'')
#%% group by test type and model
figs = [['Test_Type','MODE'],
        ['MODE']]
for fig in figs:
    grouped = subset.groupby(fig)
    for grp in grouped:
        model_counts = grp[1][['Model','Year']].drop_duplicates()['Model'].value_counts()
        grp_subset = grp[1].table.query_list('Model', model_counts[model_counts>1].index)
        if len(grp_subset)==0: continue
        name = re.sub('[(),\']','',str(grp[0])).replace(' ', '_')
        ax = sns.factorplot(x='Year', y='Chest_Clip_3ms', col='Model', 
                            kind='bar', data=grp_subset, col_wrap=3, capsize=0.3,
                            facet_kws={'subplot_kws':{'ylim': [30, 70]}})
        plt.subplots_adjust(top=0.85)
        ax.fig.suptitle(grp[0])
        ax.savefig(PATH + name + '_bymodel_TC.png')
        plt.show()
        ax = sns.factorplot(x='Year', y='Chest_Clip_3ms', kind='bar', data=grp_subset, capsize=0.3,
                            facet_kws={'subplot_kws':{'ylim': [30, 65]}})
        plt.subplots_adjust(top=0.85)
        ax.fig.suptitle(grp[0])
        ax.savefig(PATH + name + '_TC.png')
        plt.show()