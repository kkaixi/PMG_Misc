# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 13:36:28 2019

Assessing the utility of vehicle damage data

@author: tangk
"""

from PMG.read_data import PMGDataset
from PMG.COM.get_props import get_peaks
#import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


directory = 'P:\\Data Analysis\\Projects\\Misc\\Vehicle_Damage_Test\\'
cutoff = range(100, 1600)
channels = ['11HEAD0000THACXA','11HEAD0000THACYA','11HEAD0000THACZA',
            '11NECKUP00THFOXA','11NECKUP00THFOYA','11NECKUP00THFOZA',
            '11NECKLO00THFOXA','11NECKLO00THFOYA','11NECKLO00THFOZA',
            '11CHST0000THACXC','11CHST0000THACYC','11CHST0000THACZC',
            '11CHSTLEUPTHDSXB','11CHSTLELOTHDSXB','11CHSTRIUPTHDSXB','11CHSTRILOTHDSXB',
            '11LUSP0000THFOXA','11LUSP0000THFOYA','11LUSP0000THFOZA',
            '11ILACLE00THFOXA','11ILACRI00THFOXA',
            '11PELV0000THACXA','11PELV0000THACYA','11PELV0000THACZA',
            '11FEMRLE00THFOZB','11FEMRRI00THFOZB',
            '11HEAD0000H3ACXA','11HEAD0000H3ACYA','11HEAD0000H3ACZA',
            '11NECKUP00H3FOXA','11NECKUP00H3FOYA','11NECKUP00H3FOZA',
            '11CHST0000H3ACXC','11CHST0000H3ACYC','11CHST0000H3ACZC',
            '11CHST0000H3DSXB',
            '11PELV0000H3ACXA','11PELV0000H3ACYA','11PELV0000H3ACZA',
            '11FEMRLE00H3FOZB','11FEMRRI00H3FOZB',
            '11SEBE0000B3FO0D','11SEBE0000B6FO0D',
            '10SIMELE00INACXD','10SIMERI00INACXD','10CVEHCG0000ACXD']
table_filters = {'query': 'SPEED==48',
                 'drop': ['TC13-024']}
preprocessing = None


#%% initialize the dataset and specify channels, filters, and preprocessing
dataset = PMGDataset(directory, channels=channels, cutoff=cutoff, verbose=False)
dataset.table_filters = table_filters
dataset.preprocessing = preprocessing

dataset.get_data(['timeseries'])
features = get_peaks(dataset.timeseries)
features.at['TC18-212', 'Min_10SIMERI00INACXD'] = np.nan
features.at['TC18-030', 'Min_10SIMELE00INACXD'] = np.nan
#%% plot 
# columns are WHEEL, A_PILLAR, CROSS_MEMBER_BEND, IP_INTRUSION,
# DOOR_A_PILLAR, DOOR_B_PILLAR, DOOR, ROOF_FOLDING, SIDE_AIRBAG_DEPLOYED
plot_channels = ['10SIMELE00INACXD',
                 '10CVEHCG0000ACXD',
                 '11SEBE0000B6FO0D']
col = 'CROSS_MEMBER_BEND'

for ch in plot_channels:
    fig, ax = plt.subplots()
    
    x = np.concatenate(dataset.timeseries[ch].values)
    t = np.tile(dataset.t, len(dataset.timeseries))
    cond = np.repeat(dataset.table[col], len(dataset.t))
    
    ax = sns.lineplot(x='t', y='x', hue='cond', data=pd.DataFrame({'t': t, 'x': x, 'cond': cond}))
    ax.set_title((col, ch))
    
#%% plot peaks

plot_channels = ['Min_11HEAD0000THACXA',
                 'Min_11NECKUP00THFOXA',
                 'Min_11NECKLO00THFOXA',
                 'Min_11CHST0000THACXC',
                 'Min_11CHSTLEUPTHDSXB',
                 'Min_11CHSTLELOTHDSXB',
                 'Min_11CHSTRIUPTHDSXB',
                 'Min_11CHSTRILOTHDSXB',
                 'Min_11LUSP0000THFOXA',
                 'Max_11LUSP0000THFOXA',
                 'Min_11LUSP0000THFOZA',
                 'Max_11LUSP0000THFOZA',
                 'Min_11ILACLE00THFOXA',
                 'Min_11PELV0000THACXA',
                 'Min_11FEMRLE00THFOZB',
                 'Min_11FEMRRI00THFOZB',
                 'Max_11SEBE0000B3FO0D',
                 'Max_11SEBE0000B6FO0D',
                 'Min_10CVEHCG0000ACXD',
                 'Min_10SIMELE00INACXD',
                 'Min_10SIMERI00INACXD',
                 'Min_11HEAD0000THACYA',
                 'Max_11HEAD0000THACYA']
col = 'WHEEL'
for ch in plot_channels:
    fig, ax = plt.subplots()
    x = features.loc[dataset.table.index, ch]
    cond = dataset.table[col]
#    ax = sns.barplot(x='cond', y='ch', data=pd.DataFrame({'ch': x, 'cond': cond}), order=['None','Detached','Rim Damage'])
    ax = sns.barplot(x='cond', y='ch', data=pd.DataFrame({'ch': x, 'cond': cond}))
    ax.set_title(ch)
    
#%%
cols = np.array(['WHEEL', 'A_PILLAR', 'CROSS_MEMBER_BEND', 
                 'IP_INTRUSION', 'DOOR_A_PILLAR', 'DOOR_B_PILLAR', 
                 'ROOF_FOLDING'])

for i in range(len(cols)-1):
    for j in range(i+1, len(cols)):
        print(dataset.table.groupby([cols[i], cols[j]]).count()['MODEL'])
        print('\n')

#%% compare deformations at different points
plot_channels = ['Min_10SIMELE00INACXD',
                 'Min_10CVEHCG0000ACXD',
                 'Min_10SIMERI00INACXD']
cols = ['A_PILLAR','DOOR_A_PILLAR','DOOR_B_PILLAR','ROOF_FOLDING']
for ch in plot_channels:
    data = (dataset.table[cols]
                   .reset_index()
                   .melt(id_vars=['TC'], value_vars=cols)
                   .replace({0:np.nan})
                   .dropna())
    data[ch] = data[['TC','value']].apply(lambda x: features.at[x['TC'], ch], axis=1)
    data = data.set_index('TC')
    fig, ax = plt.subplots()
    ax = sns.barplot(x='variable', y=ch, ax=ax, data=data)
#    ax = sns.catplot(x='variable', y=ch, ax=ax, data=data, color='#000000')
    plt.show()
    plt.close(fig)
    
#%% compare combinations of deformations
plot_channels = ['Min_10SIMELE00INACXD',
                 'Min_10CVEHCG0000ACXD',
                 'Min_10SIMERI00INACXD']
cols = ['A_PILLAR','DOOR_A_PILLAR','DOOR_B_PILLAR','ROOF_FOLDING']

def_key = {x[1]: x[0] for x in enumerate(dataset.table[cols].drop_duplicates().apply(tuple, axis=1))}

for ch in plot_channels:
    data = pd.concat((dataset.table[cols].apply(lambda x: def_key[tuple(x)], axis=1).rename('x'), features[ch]), axis=1)
    fig, ax = plt.subplots()
    ax = sns.barplot(x='x', y=ch, ax=ax, data=data)
    ax = sns.catplot(x='x', y=ch, ax=ax, data=data, color='#000000')
#%% compare number of deformations with vehicle response
plot_channels = ['Min_10SIMELE00INACXD',
                 'Min_10CVEHCG0000ACXD',
                 'Min_10SIMERI00INACXD']
cols = ['A_PILLAR','DOOR_A_PILLAR','DOOR_B_PILLAR','ROOF_FOLDING']
for ch in plot_channels:
    data = pd.concat((dataset.table[cols].sum(axis=1), features[ch]), axis=1)
    data = data.rename({0: 'num_deform'}, axis=1)
    fig, ax = plt.subplots()
    ax = sns.barplot(x='num_deform', y=ch, ax=ax, data=data)
    ax = sns.catplot(x='num_deform', y=ch, ax=ax, data=data, color='#000000')
#    ax = sns.regplot(x='num_deform', y=ch, ax=ax, data=data)
